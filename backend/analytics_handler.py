import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import asyncio
from collections import defaultdict, Counter
import sqlite3
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsHandler:
    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for analytics storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                user_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                properties TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                page_views INTEGER DEFAULT 0,
                events_count INTEGER DEFAULT 0,
                user_agent TEXT,
                referrer TEXT,
                UNIQUE(user_id, session_id)
            )
        ''')
        
        # Create user_insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL UNIQUE,
                first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_sessions INTEGER DEFAULT 0,
                total_events INTEGER DEFAULT 0,
                resumes_uploaded INTEGER DEFAULT 0,
                analyses_completed INTEGER DEFAULT 0,
                avg_match_score REAL DEFAULT 0,
                top_skills TEXT,
                user_status TEXT DEFAULT 'active'
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_event_name ON events(event_name)')
        
        conn.commit()
        conn.close()
        logger.info("Analytics database initialized successfully")

    async def process_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a batch of analytics events"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            processed_count = 0
            user_insights_updates = defaultdict(dict)
            
            for event in events:
                # Extract event data
                event_name = event.get('event')
                user_id = event.get('userId')
                properties = event.get('properties', {})
                session_id = properties.get('sessionId')
                timestamp = datetime.fromtimestamp(event.get('timestamp', 0) / 1000, tz=timezone.utc)
                
                if not all([event_name, user_id, session_id]):
                    logger.warning(f"Skipping invalid event: {event}")
                    continue
                
                # Insert event
                cursor.execute('''
                    INSERT INTO events (event_name, user_id, session_id, properties, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (event_name, user_id, session_id, json.dumps(properties), timestamp))
                
                # Update session tracking
                cursor.execute('''
                    INSERT OR REPLACE INTO user_sessions 
                    (user_id, session_id, start_time, page_views, events_count, user_agent, referrer)
                    VALUES (?, ?, ?, 
                        COALESCE((SELECT page_views FROM user_sessions WHERE user_id=? AND session_id=?), 0) + ?,
                        COALESCE((SELECT events_count FROM user_sessions WHERE user_id=? AND session_id=?), 0) + 1,
                        ?, ?)
                ''', (
                    user_id, session_id, timestamp,
                    user_id, session_id, 1 if event_name == 'page_viewed' else 0,
                    user_id, session_id,
                    properties.get('userAgent', ''),
                    properties.get('referrer', '')
                ))
                
                # Collect data for user insights updates
                self._update_user_insights_data(user_insights_updates, user_id, event_name, properties, timestamp)
                
                processed_count += 1
            
            # Batch update user insights
            await self._batch_update_user_insights(cursor, user_insights_updates)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Processed {processed_count} analytics events successfully")
            
            return {
                'success': True,
                'processed_count': processed_count,
                'message': f'Successfully processed {processed_count} events'
            }
            
        except Exception as e:
            logger.error(f"Error processing analytics events: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processed_count': 0
            }

    def _update_user_insights_data(self, insights_data: Dict, user_id: str, event_name: str, properties: Dict, timestamp: datetime):
        """Collect data for user insights updates"""
        if user_id not in insights_data:
            insights_data[user_id] = {
                'last_seen': timestamp,
                'events_count': 0,
                'resumes_uploaded': 0,
                'analyses_completed': 0,
                'match_scores': [],
                'skills': []
            }
        
        data = insights_data[user_id]
        data['events_count'] += 1
        data['last_seen'] = max(data['last_seen'], timestamp)
        
        # Track specific events
        if event_name == 'resume_uploaded':
            data['resumes_uploaded'] += 1
        elif event_name == 'analysis_completed':
            data['analyses_completed'] += 1
            match_score = properties.get('matchScore')
            if match_score:
                data['match_scores'].append(match_score)
        elif event_name == 'feature_usage':
            feature = properties.get('feature')
            if feature:
                data['skills'].append(feature)

    async def _batch_update_user_insights(self, cursor, insights_data: Dict):
        """Batch update user insights"""
        for user_id, data in insights_data.items():
            avg_match_score = sum(data['match_scores']) / len(data['match_scores']) if data['match_scores'] else 0
            top_skills = json.dumps(list(Counter(data['skills']).most_common(5)))
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_insights 
                (user_id, first_seen, last_seen, total_events, resumes_uploaded, 
                 analyses_completed, avg_match_score, top_skills)
                VALUES (?, 
                    COALESCE((SELECT first_seen FROM user_insights WHERE user_id=?), ?),
                    ?, 
                    COALESCE((SELECT total_events FROM user_insights WHERE user_id=?), 0) + ?,
                    COALESCE((SELECT resumes_uploaded FROM user_insights WHERE user_id=?), 0) + ?,
                    COALESCE((SELECT analyses_completed FROM user_insights WHERE user_id=?), 0) + ?,
                    ?, ?)
            ''', (
                user_id, user_id, data['last_seen'], data['last_seen'],
                user_id, data['events_count'],
                user_id, data['resumes_uploaded'],
                user_id, data['analyses_completed'],
                avg_match_score, top_skills
            ))

    def get_analytics_dashboard(self, time_range: str = '7d') -> Dict[str, Any]:
        """Get analytics dashboard data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Define time filter
            if time_range == '24h':
                time_filter = "timestamp > datetime('now', '-1 day')"
            elif time_range == '7d':
                time_filter = "timestamp > datetime('now', '-7 days')"
            elif time_range == '30d':
                time_filter = "timestamp > datetime('now', '-30 days')"
            else:
                time_filter = "1=1"  # All time
            
            # Get basic metrics
            cursor.execute(f'''
                SELECT 
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(DISTINCT session_id) as sessions,
                    COUNT(*) as total_events
                FROM events 
                WHERE {time_filter}
            ''')
            basic_metrics = cursor.fetchone()
            
            # Get popular events
            cursor.execute(f'''
                SELECT event_name, COUNT(*) as count
                FROM events 
                WHERE {time_filter}
                GROUP BY event_name
                ORDER BY count DESC
                LIMIT 10
            ''')
            popular_events = cursor.fetchall()
            
            # Get conversion metrics
            cursor.execute(f'''
                SELECT 
                    SUM(CASE WHEN event_name = 'resume_uploaded' THEN 1 ELSE 0 END) as resumes_uploaded,
                    SUM(CASE WHEN event_name = 'analysis_completed' THEN 1 ELSE 0 END) as analyses_completed,
                    COUNT(DISTINCT CASE WHEN event_name = 'resume_uploaded' THEN user_id END) as users_uploaded,
                    COUNT(DISTINCT CASE WHEN event_name = 'analysis_completed' THEN user_id END) as users_analyzed
                FROM events 
                WHERE {time_filter}
            ''')
            conversion_metrics = cursor.fetchone()
            
            # Get hourly activity (last 24 hours)
            cursor.execute('''
                SELECT 
                    strftime('%H', timestamp) as hour,
                    COUNT(*) as events_count
                FROM events 
                WHERE timestamp > datetime('now', '-1 day')
                GROUP BY hour
                ORDER BY hour
            ''')
            hourly_activity = cursor.fetchall()
            
            # Get top user insights
            cursor.execute('''
                SELECT 
                    user_id,
                    total_events,
                    resumes_uploaded,
                    analyses_completed,
                    avg_match_score,
                    top_skills
                FROM user_insights
                ORDER BY total_events DESC
                LIMIT 10
            ''')
            top_users = cursor.fetchall()
            
            conn.close()
            
            # Calculate conversion rates
            conversion_rate = 0
            if conversion_metrics[2] > 0:  # users_uploaded
                conversion_rate = (conversion_metrics[3] / conversion_metrics[2]) * 100  # users_analyzed / users_uploaded
            
            return {
                'success': True,
                'data': {
                    'basic_metrics': {
                        'unique_users': basic_metrics[0],
                        'sessions': basic_metrics[1],
                        'total_events': basic_metrics[2]
                    },
                    'conversion_metrics': {
                        'resumes_uploaded': conversion_metrics[0],
                        'analyses_completed': conversion_metrics[1],
                        'users_uploaded': conversion_metrics[2],
                        'users_analyzed': conversion_metrics[3],
                        'conversion_rate': round(conversion_rate, 2)
                    },
                    'popular_events': [{'event': row[0], 'count': row[1]} for row in popular_events],
                    'hourly_activity': [{'hour': row[0], 'events': row[1]} for row in hourly_activity],
                    'top_users': [
                        {
                            'user_id': row[0],
                            'total_events': row[1],
                            'resumes_uploaded': row[2],
                            'analyses_completed': row[3],
                            'avg_match_score': row[4],
                            'top_skills': json.loads(row[5]) if row[5] else []
                        } for row in top_users
                    ]
                },
                'time_range': time_range
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics dashboard: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights for a specific user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user summary
            cursor.execute('''
                SELECT * FROM user_insights WHERE user_id = ?
            ''', (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return {'success': False, 'error': 'User not found'}
            
            # Get recent events
            cursor.execute('''
                SELECT event_name, properties, timestamp
                FROM events 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (user_id,))
            recent_events = cursor.fetchall()
            
            # Get session summary
            cursor.execute('''
                SELECT COUNT(*) as session_count, 
                       SUM(page_views) as total_page_views,
                       AVG(events_count) as avg_events_per_session
                FROM user_sessions 
                WHERE user_id = ?
            ''', (user_id,))
            session_summary = cursor.fetchone()
            
            conn.close()
            
            return {
                'success': True,
                'user_insights': {
                    'user_id': user_data[1],
                    'first_seen': user_data[2],
                    'last_seen': user_data[3],
                    'total_sessions': session_summary[0] if session_summary else 0,
                    'total_events': user_data[5],
                    'total_page_views': session_summary[1] if session_summary else 0,
                    'avg_events_per_session': round(session_summary[2], 2) if session_summary and session_summary[2] else 0,
                    'resumes_uploaded': user_data[6],
                    'analyses_completed': user_data[7],
                    'avg_match_score': user_data[8],
                    'top_skills': json.loads(user_data[9]) if user_data[9] else [],
                    'user_status': user_data[10]
                },
                'recent_events': [
                    {
                        'event': row[0],
                        'properties': json.loads(row[1]) if row[1] else {},
                        'timestamp': row[2]
                    } for row in recent_events
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting user insights: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Global analytics handler instance
analytics_handler = AnalyticsHandler()

async def process_analytics_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Main function to process analytics events"""
    return await analytics_handler.process_events(events)

def get_analytics_dashboard(time_range: str = '7d') -> Dict[str, Any]:
    """Get analytics dashboard data"""
    return analytics_handler.get_analytics_dashboard(time_range)

def get_user_insights(user_id: str) -> Dict[str, Any]:
    """Get user insights"""
    return analytics_handler.get_user_insights(user_id) 