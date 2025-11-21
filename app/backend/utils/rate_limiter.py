"""
Rate limiter to prevent API abuse and control costs
"""
import time
from collections import defaultdict

# Track requests per IP
_request_counts = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 10
MAX_REQUESTS_PER_HOUR = 50

def is_rate_limited(ip_address):
    """
    Check if IP is rate limited
    Returns: (is_limited, reason)
    """
    now = time.time()
    
    # Clean old entries
    _request_counts[ip_address] = [
        ts for ts in _request_counts[ip_address]
        if now - ts < 3600  # Keep last hour
    ]
    
    requests = _request_counts[ip_address]
    
    # Check per-minute limit
    recent_requests = [ts for ts in requests if now - ts < 60]
    if len(recent_requests) >= MAX_REQUESTS_PER_MINUTE:
        return True, f"Rate limit exceeded: {MAX_REQUESTS_PER_MINUTE} requests per minute"
    
    # Check per-hour limit
    if len(requests) >= MAX_REQUESTS_PER_HOUR:
        return True, f"Rate limit exceeded: {MAX_REQUESTS_PER_HOUR} requests per hour"
    
    return False, None

def record_request(ip_address):
    """Record a request for rate limiting"""
    _request_counts[ip_address].append(time.time())

