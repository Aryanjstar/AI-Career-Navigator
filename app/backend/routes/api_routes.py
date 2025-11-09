"""
API Routes for AI Career Navigator
"""
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from services.ai_service import AIService
from utils.file_processor import extract_text_from_file
from config import Config

logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Initialize AI Service
ai_service = AIService()


@api_bp.route('/config')
def get_config():
    """API configuration endpoint"""
    return jsonify({
        "platform": "MERN Stack Career Navigator",
        "version": "2.0.0",
        "ai": {
            "model": Config.AZURE_OPENAI_MODEL,
            "deployment": Config.AZURE_OPENAI_DEPLOYMENT,
            "endpoint_configured": bool(Config.AZURE_OPENAI_ENDPOINT),
            "api_key_configured": bool(Config.AZURE_OPENAI_API_KEY)
        },
        "features": {
            "career_chat": True,
            "resume_analysis": True,
            "interview_prep": True,
            "skill_assessment": True
        },
        "tech_stack": ["MongoDB", "Express.js", "React", "Node.js", "Python", "Azure OpenAI"],
        "developer": {
            "name": "Aryan Jaiswal",
            "email": "aryanjstar3@gmail.com",
            "linkedin": "https://www.linkedin.com/in/aryanjstar",
            "github": "https://github.com/Aryanjstar/AI-Career-Navigator"
        }
    })


@api_bp.route('/api/career-chat', methods=['POST'])
def career_chat():
    """Handle career guidance chat"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_role = data.get('user_role', '')
        experience = data.get('experience', '')
        focus_area = data.get('focus_area', '')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Validate that all three selections are made
        if not user_role or not experience or not focus_area:
            return jsonify({
                "response": "👋 Hi there! I'm excited to help you with your career journey! However, I need to know more about you first. Please select your **Role**, **Experience Level**, and **Focus Area** from the dropdowns above so I can provide personalized guidance tailored specifically to your career goals. Once you've made all three selections, I'll be ready to assist you! 🚀"
            })
        
        # Additional validation for default/placeholder values
        default_values = ['Select Role', 'Select Experience', 'Select Focus Area', 'Choose Role', 'Choose Experience', 'Choose Focus Area']
        if user_role in default_values or experience in default_values or focus_area in default_values:
            return jsonify({
                "response": "👋 Hi there! I'm excited to help you with your career journey! However, I need to know more about you first. Please select your **Role**, **Experience Level**, and **Focus Area** from the dropdowns above so I can provide personalized guidance tailored specifically to your career goals. Once you've made all three selections, I'll be ready to assist you! 🚀"
            })
        
        # Check for simple greetings and respond appropriately
        greeting_words = ['hi', 'hii', 'hello', 'hey', 'hiya', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if user_message.lower().strip() in greeting_words:
            return jsonify({
                "response": f"👋 Hello! I'm your AI Career Navigator, and I'm here to help you excel as a **{user_role}** at the **{experience}** level with a focus on **{focus_area}**! \n\nI can assist you with:\n• Career guidance and growth strategies\n• Technical skill development\n• Job search and interview preparation\n• Industry insights and trends\n• MERN stack expertise\n\n💬 What would you like to discuss today? Feel free to ask me anything about your career journey!"
            })
        
        # Create contextual prompt
        prompt = f"""
**Act as an expert AI Career Mentor for the tech industry.**

**User's Profile:**
- **Current/Target Role:** {user_role}
- **Experience Level:** {experience}
- **Primary Goal for this Conversation:** {focus_area}

**User's Question:** "{user_message}"

**Your Task:**
Provide a comprehensive, in-depth, and actionable response that is STRICTLY tailored to the user's profile above. Do not give generic advice. Address the user directly as "you". **Do not invent, use, or ask for the user's name.**

**Response Structure:**
1.  **Direct Answer & Insight:** Start with a direct answer to the user's question, providing a core insight based on their specific profile.
2.  **Strategic Breakdown:** Based on their '{experience}' experience and '{focus_area}' goal, break down the advice into logical, strategic steps. Use bullet points for clarity.
3.  **Contextual Examples:** Provide concrete examples relevant to a '{user_role}'. For instance, if they ask about projects, suggest project ideas that align with their role and experience.
4.  **Potential Pitfalls & Pro-Tips:** Mention 1-2 common mistakes someone with their profile might make and how to avoid them.
5.  **Next Steps:** Suggest 2-3 clear, actionable next steps the user can take this week.

Maintain a professional, encouraging, and mentoring tone.
"""
        
        response = ai_service.get_completion(prompt, max_tokens=3000)
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/api/resume-analysis', methods=['POST'])
def resume_analysis():
    """Analyze resume for ATS optimization - handles both file upload and text input"""
    try:
        resume_text = ""
        
        # Check if this is a file upload (multipart/form-data)
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            # Handle file upload
            if 'resume_file' in request.files:
                file = request.files['resume_file']
                if file.filename != '':
                    try:
                        # Extract text from uploaded file (PDF, DOC, DOCX, TXT)
                        resume_text = extract_text_from_file(file)
                    except Exception as e:
                        return jsonify({
                            "error": f"Failed to read file: {str(e)}. Please try a different file or copy-paste your resume text."
                        }), 400
            
            # Also check for text in form data (if both file and text provided, text takes precedence)
            form_text = request.form.get('resume_text', '').strip()
            if form_text:
                resume_text = form_text
                
        else:
            # Handle JSON request (text only)
            data = request.get_json()
            if data:
                resume_text = data.get('resume_text', '').strip()
        
        if not resume_text:
            return jsonify({"error": "Resume text is required. Please either upload a file (PDF/DOC/DOCX/TXT) or paste your resume text."}), 400
        

        # Resume analysis
        prompt = f"""
        **Act as a world-class Senior Technical Recruiter and ATS (Applicant Tracking System) expert.** Your user is applying for technical roles, likely related to MERN stack development.

        **Analyze the following resume content thoroughly:**
        ---
        {resume_text}
        ---

        **Your Task:**
        Provide a comprehensive, in-depth resume review with the goal of dramatically increasing its effectiveness for landing interviews.

        **Required Analysis Sections (Be Detailed):**

        1.  **Overall ATS & Recruiter Score:** Give a score out of 10 and a brief justification for it.
        2.  **First Impression (The 6-Second Test):** What is a human recruiter's immediate takeaway in the first 6 seconds? Is the key information (name, role, key skills) immediately obvious and impressive?
        3.  **Strengths & High-Impact Areas:** Point out 1-2 specific sections or bullet points that are strong and explain precisely why they work well.
        4.  **Critical Improvement Areas & Justification:**
            * **Keywords & Skills:** Are essential tech skills (e.g., React, Node.js, Express, MongoDB, TypeScript, CI/CD, Docker, AWS/Azure) missing or underrepresented? Provide a list of specific keywords they should add and suggest where to place them.
            * **Action Verbs & Impact Metrics:** Are the bullet points passive ("responsible for...") or active ("developed, optimized, led...")? Do they show quantifiable impact (e.g., "Increased performance by 30%" instead of "Worked on performance improvements")? **Rewrite 1-2 of the user's existing bullet points** to demonstrate this powerful principle.
            * **Formatting & Readability:** Is the resume clean, modern, and easy to parse for both ATS and humans? Comment on whitespace, font choice/size, and overall layout.
        5.  **Actionable Plan for Improvement:** Provide a prioritized list of the top 3-5 actions the user must take to improve their resume, explaining the high-value impact of each action.
        """
        
        analysis = ai_service.get_completion(prompt, max_tokens=3000)
        
        return jsonify({
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/api/interview-prep', methods=['POST'])
def interview_prep():
    """Generate interview questions and preparation tips"""
    try:
        data = request.get_json()
        role = data.get('role', '')
        target_company = data.get('target_company', '')
        company_size = data.get('company_size', '')
        
        # Validate that all required fields are provided
        if not role or not target_company or not company_size:
            return jsonify({
                "response": "👋 Hello! I'm here to help you prepare for your interview! However, I need some details first. Please select your Role, Target Company, and Company Size from the dropdowns above so I can provide personalized interview preparation guidance. Once you've made all three selections, I'll help you ace that interview! 🎯"
            })
        
        # Additional validation for default/placeholder values
        default_values = ['Select Role', 'Select Company', 'Select Company Size', 'Choose Role', 'Choose Company', 'Choose Company Size', 'Click to select']
        if role in default_values or target_company in default_values or company_size in default_values:
            return jsonify({
                "response": "👋 Hello! I'm here to help you prepare for your interview! However, I need some details first. Please select your **Role**, **Target Company**, and **Company Size** from the dropdowns above so I can provide personalized interview preparation guidance. Once you've made all three selections, I'll help you ace that interview! 🎯"
            })
            
        # Check for simple greetings and respond appropriately
        greeting_words = ['hi', 'hii', 'hello', 'hey', 'hiya', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if role.lower() in greeting_words or target_company.lower() in greeting_words or company_size.lower() in greeting_words:
            return jsonify({
                "response": "👋 Hi there! I'm excited to help you prepare for your interview! Let's make sure you're fully prepared and confident. What specific aspects of the interview would you like to focus on?"
            })
        
        #Interview prep 
        prompt = f"""
        **Act as an experienced Interview Coach for '{target_company}'.** Prepare this candidate for their {role} interview.

        **Profile:**
        - **Role:** {role}
        - **Company:** {target_company}
        - **Type:** {company_size}

        **Generate a complete interview preparation guide with these sections:**

        <h4><strong>Company-Specific Insights</strong></h4>
        <p>What {target_company} values for {role} positions and what they'll likely focus on during interviews.</p>

        <h4><strong>Technical Questions You Should Expect</strong></h4>
        <ul>
        <li><strong>Question 1:</strong> [Specific technical question relevant to {role}]</li>
        <li><strong>What they're testing:</strong> [Explain the concept being evaluated]</li>
        <li><strong>Question 2:</strong> [Another role-specific technical question]</li>
        <li><strong>What they're testing:</strong> [Explain the skill being assessed]</li>
        </ul>

        <h4><strong>Behavioral Question + S.T.A.R. Method</strong></h4>
        <p><strong>Expected Question:</strong> [One challenging behavioral question for {role}]</p>
        <p><strong>How to Answer:</strong> Use S.T.A.R. (Situation, Task, Action, Result) structure. [Brief explanation of why this works]</p>

        <h4><strong>Smart Questions to Ask Them</strong></h4>
        <ul>
        <li>[Question that shows genuine interest in the role/team]</li>
        <li>[Question about technical challenges or growth]</li>
        <li>[Question about success metrics or team dynamics]</li>
        </ul>

        <h4><strong>48-Hour Prep Checklist</strong></h4>
        <ul>
        <li>[Key preparation step]</li>
        <li>[Important thing to review]</li>
        <li>[Final confidence booster]</li>
        </ul>

        Keep it practical and actionable. Focus on what matters most for {role} at {target_company}.
        """
        
        response_text = ai_service.get_completion(prompt, max_tokens=6000)
        
        return jsonify({
            "response": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Interview prep error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/api/skill-analysis', methods=['POST'])
def skill_analysis():
    """Analyze skill gaps and provide learning roadmap"""
    try:
        data = request.get_json()
        target_role = data.get('target_role', '')
        current_skills = data.get('current_skills', '')
        
        if not target_role or not current_skills:
            return jsonify({"error": "Target role and current skills are required"}), 400
        
        # Skill Gap
        
        prompt = f"""
        **Act as a Senior Engineer and a supportive Tech Mentor.**

        **User's Goal:**
        - **Target Role:** {target_role}
        - **Current Skills:** {current_skills}

        **Your Task:**
        Generate the content for the user's skill gap analysis. Your entire response **MUST** start directly with the "Executive Summary" heading as shown below. Do not add any other titles or introductory text before it. Follow the section structure precisely.

        **Required Sections:**

        <h4><strong>Executive Summary</strong></h4>
        <p>[Provide a concise paragraph summarizing the primary gap and offering encouragement.]</p>

        <h4><strong>Detailed Skill Gap Analysis</strong></h4>
        <ul>
            <li><strong>Skills You Have:</strong> [Acknowledge the user's current skills and their relevance.]</li>
            <li><strong>Critical Missing Skills:</strong> [Identify 'Must-Have' and 'Good-to-Have' skills, explaining the importance of each for the target role.]</li>
        </ul>

        <h4><strong>Structured Learning Roadmap</strong></h4>
        <p>[Break the plan into logical, time-based phases. For each skill, recommend 1-2 specific, high-quality resources with clickable URLs. Suggest a detailed capstone project idea.]</p>

        <h4><strong>Market & Salary Insights</strong></h4>
        <p>[Provide a realistic salary range and comment on market demand for the target role.]</p>
        """
        
        analysis = ai_service.get_completion(prompt, max_tokens=2000)
        
        return jsonify({
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Skill analysis error: {e}")
        return jsonify({"error": "Internal server error"}), 500

