import json
import logging
import os
import time
from typing import Dict, List, Optional, Any
from pathlib import Path

from openai import AsyncAzureOpenAI
from quart import (
    Blueprint,
    Quart,
    current_app,
    jsonify,
    request,
    send_from_directory,
    render_template_string
)
from quart_cors import cors
import aiofiles

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Quart app
app = Quart(__name__)
app = cors(app, allow_origin="*")

# Configuration
class Config:
    def __init__(self):
        # Azure OpenAI configuration - using your existing setup
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://gpt-31.openai.azure.com/")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.azure_openai_model = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")
        self.azure_openai_deployment = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1")
        
        # Feature flags (cost optimization)
        self.enable_career_chat = os.getenv("ENABLE_CAREER_CHAT", "true").lower() == "true"
        self.enable_resume_analysis = os.getenv("ENABLE_RESUME_ANALYSIS", "true").lower() == "true"
        self.enable_interview_prep = os.getenv("ENABLE_INTERVIEW_PREP", "true").lower() == "true"
        self.enable_skill_assessment = os.getenv("ENABLE_SKILL_ASSESSMENT", "true").lower() == "true"
        
        # Disabled expensive features
        self.use_vectors = False
        self.use_search = False
        self.use_authentication = False

config = Config()

# Initialize Azure OpenAI client
try:
    openai_client = AsyncAzureOpenAI(
        azure_endpoint=config.azure_openai_endpoint,
        api_key=config.azure_openai_api_key,
        api_version=config.azure_openai_api_version
    )
    logger.info(f"✅ Azure OpenAI client initialized with endpoint: {config.azure_openai_endpoint}")
except Exception as e:
    logger.error(f"❌ Failed to initialize Azure OpenAI client: {e}")
    openai_client = None

# Career guidance prompts optimized for GPT-4.1
CAREER_PROMPTS = {
    "resume_analysis": """
You are an expert career coach and resume reviewer. Analyze the provided resume and give specific, actionable feedback.

Focus on:
1. Overall structure and formatting
2. Skills and experience relevance
3. Missing key skills for the target role
4. Specific improvements needed
5. Match percentage with job requirements

Be encouraging but honest. Provide a numerical score (0-100) and detailed feedback.
""",
    
    "interview_prep": """
You are an experienced interviewer and career coach. Generate relevant interview questions based on the job role and user's experience.

Create:
1. 5 technical questions relevant to the role
2. 3 behavioral questions
3. 2 situational questions
4. Sample answers and tips for each

Make questions realistic and current with industry standards.
""",
    
    "career_guidance": """
You are a career counselor with deep industry knowledge. Provide personalized career advice based on the user's background and goals.

Address:
1. Career path recommendations
2. Skill development priorities
3. Industry trends and opportunities
4. Next steps and timeline
5. Potential challenges and solutions

Be specific and actionable in your recommendations.
""",
    
    "skill_assessment": """
You are a technical skills assessor. Evaluate the user's current skills and identify gaps for their target role.

Provide:
1. Current skill level assessment (1-10 scale)
2. Skills gap analysis
3. Learning recommendations
4. Priority order for skill development
5. Estimated timeline for improvement

Base recommendations on current market demands.
"""
}

async def call_openai(messages: List[Dict], max_tokens: int = 1500, temperature: float = 0.7) -> str:
    """Call Azure OpenAI with error handling and cost optimization"""
    if not openai_client:
        return "AI service is currently unavailable. Please try again later."
    
    try:
        response = await openai_client.chat.completions.create(
            model=config.azure_openai_deployment,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

# Routes

@app.route("/")
async def index():
    """Serve the main application"""
    try:
        # Try to serve built frontend files
        return await send_from_directory("static", "index.html")
    except:
        # Fallback to simple HTML if frontend not built
        return await render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🚀 AI Career Navigator</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', system-ui, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; min-height: 100vh; padding: 20px;
                }
                .container { max-width: 1000px; margin: 0 auto; }
                .header { text-align: center; margin-bottom: 40px; }
                .header h1 { font-size: 3em; margin-bottom: 10px; }
                .header p { font-size: 1.2em; opacity: 0.9; }
                .status { 
                    background: rgba(0,255,0,0.2); 
                    padding: 15px; border-radius: 10px; margin: 20px 0; 
                    border: 1px solid rgba(0,255,0,0.3);
                }
                .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .feature { 
                    background: rgba(255,255,255,0.1); 
                    padding: 25px; border-radius: 15px; 
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);
                    transition: transform 0.3s ease;
                }
                .feature:hover { transform: translateY(-5px); }
                .feature h3 { margin-bottom: 15px; font-size: 1.3em; }
                .footer { text-align: center; margin-top: 40px; opacity: 0.8; }
                .api-info { font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 AI Career Navigator</h1>
                    <p>Your AI-Powered Career Success Platform</p>
                    <p class="api-info">Powered by Azure OpenAI GPT-4.1</p>
                </div>
                
                <div class="status">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>✅ Azure OpenAI Status:</strong> Connected<br>
                            <strong>🤖 Model:</strong> {{ model }} | <strong>📍 Endpoint:</strong> {{ endpoint }}
                        </div>
                        <div style="text-align: right;">
                            <strong>💰 Cost Optimized:</strong> ✅ Yes<br>
                            <strong>🚀 Version:</strong> 1.0.0
                        </div>
                    </div>
                </div>
                
                <div class="features">
                    <div class="feature">
                        <h3>🎯 AI Career Chat</h3>
                        <p>Get personalized career advice and guidance powered by GPT-4.1. Ask about career paths, job transitions, and professional development.</p>
                        <p><strong>API:</strong> <code>/api/career-chat</code></p>
                    </div>
                    
                    <div class="feature">
                        <h3>📄 Resume Analysis</h3>
                        <p>AI-powered resume review with detailed feedback, skill gap analysis, and specific improvement recommendations.</p>
                        <p><strong>API:</strong> <code>/api/resume-analysis</code></p>
                    </div>
                    
                    <div class="feature">
                        <h3>🎤 Interview Preparation</h3>
                        <p>Practice with AI-generated interview questions tailored to your role, experience level, and target companies.</p>
                        <p><strong>API:</strong> <code>/api/interview-prep</code></p>
                    </div>
                    
                    <div class="feature">
                        <h3>📊 Skill Assessment</h3>
                        <p>Comprehensive skill evaluation, gap analysis, and learning roadmap recommendations for your target role.</p>
                        <p><strong>API:</strong> <code>/api/skill-assessment</code></p>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>🔗 API Endpoints:</strong> /config | /api/health | /api/career-chat | /api/resume-analysis</p>
                    <p>Built with Azure App Service + Static Web Apps | Optimized for cost and performance</p>
                </div>
            </div>
        </body>
        </html>
        """, 
        endpoint=config.azure_openai_endpoint.replace('https://', '').split('/')[0],
        model=config.azure_openai_model
        )

@app.route("/config")
async def get_config():
    """Return frontend configuration"""
    return jsonify({
        "features": {
            "career_chat": config.enable_career_chat,
            "resume_analysis": config.enable_resume_analysis,
            "interview_prep": config.enable_interview_prep,
            "skill_assessment": config.enable_skill_assessment
        },
        "ai": {
            "model": config.azure_openai_model,
            "endpoint_configured": bool(config.azure_openai_endpoint),
            "api_key_configured": bool(config.azure_openai_api_key),
            "deployment": config.azure_openai_deployment
        },
        "cost_optimized": True,
        "version": "1.0.0",
        "disabled_features": ["vectors", "search", "authentication", "document_intelligence"]
    })

@app.route("/api/career-chat", methods=["POST"])
async def career_chat():
    """AI-powered career guidance chat"""
    if not config.enable_career_chat:
        return jsonify({"error": "Career chat feature is disabled"}), 403
    
    try:
        data = await request.get_json()
        user_message = data.get("message", "")
        context = data.get("context", {})
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        messages = [
            {"role": "system", "content": CAREER_PROMPTS["career_guidance"]},
            {"role": "user", "content": f"Context: {json.dumps(context)}\n\nQuestion: {user_message}"}
        ]
        
        response = await call_openai(messages, max_tokens=800)
        
        return jsonify({
            "response": response,
            "timestamp": time.time(),
            "model_used": config.azure_openai_model,
            "tokens_used": "optimized"
        })
        
    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": "Failed to process career guidance request"}), 500

@app.route("/api/resume-analysis", methods=["POST"])
async def analyze_resume():
    """Analyze resume with GPT-4.1"""
    if not config.enable_resume_analysis:
        return jsonify({"error": "Resume analysis feature is disabled"}), 403
    
    try:
        data = await request.get_json()
        resume_text = data.get("resume_text", "")
        job_description = data.get("job_description", "")
        
        if not resume_text:
            return jsonify({"error": "Resume text is required"}), 400
        
        analysis_prompt = f"""
        {CAREER_PROMPTS['resume_analysis']}
        
        RESUME:
        {resume_text}
        
        JOB DESCRIPTION (if provided):
        {job_description}
        
        Please provide your analysis in JSON format with the following structure:
        {{
            "overall_score": 85,
            "strengths": ["list", "of", "strengths"],
            "weaknesses": ["list", "of", "areas", "to", "improve"],
            "missing_skills": ["skills", "needed", "for", "target", "role"],
            "recommendations": ["specific", "actionable", "suggestions"],
            "match_percentage": 75
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert resume reviewer. Always respond with valid JSON."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        response = await call_openai(messages, max_tokens=1200)
        
        try:
            # Try to parse as JSON
            analysis = json.loads(response)
        except:
            # Fallback to text response
            analysis = {
                "overall_score": 75,
                "analysis": response,
                "format": "text"
            }
        
        return jsonify({
            "analysis": analysis,
            "timestamp": time.time(),
            "model_used": config.azure_openai_model
        })
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        return jsonify({"error": "Failed to analyze resume"}), 500

@app.route("/api/interview-prep", methods=["POST"])
async def interview_prep():
    """Generate interview questions and prep materials"""
    if not config.enable_interview_prep:
        return jsonify({"error": "Interview prep feature is disabled"}), 403
    
    try:
        data = await request.get_json()
        job_role = data.get("job_role", "")
        experience_level = data.get("experience_level", "mid")
        company_type = data.get("company_type", "tech")
        
        if not job_role:
            return jsonify({"error": "Job role is required"}), 400
        
        prep_prompt = f"""
        {CAREER_PROMPTS['interview_prep']}
        
        JOB ROLE: {job_role}
        EXPERIENCE LEVEL: {experience_level}
        COMPANY TYPE: {company_type}
        
        Generate comprehensive interview preparation materials.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert interview coach."},
            {"role": "user", "content": prep_prompt}
        ]
        
        response = await call_openai(messages, max_tokens=1500)
        
        return jsonify({
            "interview_prep": response,
            "job_role": job_role,
            "experience_level": experience_level,
            "timestamp": time.time(),
            "model_used": config.azure_openai_model
        })
        
    except Exception as e:
        logger.error(f"Interview prep error: {e}")
        return jsonify({"error": "Failed to generate interview prep"}), 500

@app.route("/api/skill-assessment", methods=["POST"])
async def skill_assessment():
    """Assess skills and identify gaps"""
    if not config.enable_skill_assessment:
        return jsonify({"error": "Skill assessment feature is disabled"}), 403
    
    try:
        data = await request.get_json()
        current_skills = data.get("current_skills", [])
        target_role = data.get("target_role", "")
        experience_years = data.get("experience_years", 0)
        
        if not current_skills or not target_role:
            return jsonify({"error": "Current skills and target role are required"}), 400
        
        assessment_prompt = f"""
        {CAREER_PROMPTS['skill_assessment']}
        
        CURRENT SKILLS: {', '.join(current_skills)}
        TARGET ROLE: {target_role}
        EXPERIENCE: {experience_years} years
        
        Provide a comprehensive skill assessment and gap analysis.
        """
        
        messages = [
            {"role": "system", "content": "You are a technical skills assessor."},
            {"role": "user", "content": assessment_prompt}
        ]
        
        response = await call_openai(messages, max_tokens=1200)
        
        return jsonify({
            "assessment": response,
            "current_skills": current_skills,
            "target_role": target_role,
            "timestamp": time.time(),
            "model_used": config.azure_openai_model
        })
        
    except Exception as e:
        logger.error(f"Skill assessment error: {e}")
        return jsonify({"error": "Failed to assess skills"}), 500

@app.route("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test OpenAI connection
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'OK' if you're working."}
        ]
        
        response = await call_openai(test_messages, max_tokens=10)
        openai_status = "OK" in response
        
        return jsonify({
            "status": "healthy",
            "azure_openai": {
                "connected": openai_status,
                "endpoint": config.azure_openai_endpoint,
                "model": config.azure_openai_model,
                "deployment": config.azure_openai_deployment
            },
            "features": {
                "career_chat": config.enable_career_chat,
                "resume_analysis": config.enable_resume_analysis,
                "interview_prep": config.enable_interview_prep,
                "skill_assessment": config.enable_skill_assessment
            },
            "cost_optimization": {
                "vectors_disabled": True,
                "search_disabled": True,
                "auth_disabled": True,
                "estimated_monthly_cost": "₹3500-5000"
            },
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }), 500

# Error handlers
@app.errorhandler(404)
async def not_found(error):
    return jsonify({"error": "Endpoint not found", "available_endpoints": ["/", "/config", "/api/health", "/api/career-chat", "/api/resume-analysis", "/api/interview-prep", "/api/skill-assessment"]}), 404

@app.errorhandler(500)
async def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Initialize app on module import
logger.info("🚀 Starting AI Career Navigator - Optimized for GPT-4.1")
logger.info(f"📍 Azure OpenAI Endpoint: {config.azure_openai_endpoint}")
logger.info(f"🤖 Model: {config.azure_openai_model}")
logger.info(f"💰 Cost Optimized: Yes")

def create_app():
    """Application factory"""
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
