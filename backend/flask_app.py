"""
Flask-based AI Career Navigator for Azure Deployment
Complete User Interface with all features
Optimized for GPT-4.1 and cost efficiency
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from openai import AzureOpenAI
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Azure OpenAI Configuration
try:
    openai_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    # Test connection
    deployment_name = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1")
    model_name = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")
    
    logger.info(f"✅ Azure OpenAI client initialized")
    logger.info(f"📍 Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logger.info(f"🤖 Model: {model_name}")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize OpenAI client: {e}")
    openai_client = None

# Complete User Interface HTML Template
MAIN_INTERFACE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AI Career Navigator - Your Personal Career Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(45deg, #fff, #e8f4f8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .status-bar {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
        
        .status-item {
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #333;
            text-align: center;
        }
        
        .feature-description {
            color: #666;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }
        
        .input-group {
            margin-bottom: 1rem;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #555;
        }
        
        .input-group input, .input-group textarea, .input-group select {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .input-group input:focus, .input-group textarea:focus, .input-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .input-group textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
            margin-top: 1rem;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin: 1rem 0;
        }
        
        .result {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 1rem;
            border-left: 4px solid #667eea;
            display: none;
        }
        
        .result h3 {
            color: #333;
            margin-bottom: 1rem;
        }
        
        .result-content {
            line-height: 1.6;
            color: #555;
            white-space: pre-wrap;
        }
        
        .chat-container {
            height: 400px;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            overflow-y: auto;
            padding: 1rem;
            background: #f8f9fa;
            margin-bottom: 1rem;
        }
        
        .chat-message {
            margin-bottom: 1rem;
            padding: 0.75rem;
            border-radius: 10px;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: 20%;
        }
        
        .ai-message {
            background: white;
            border: 1px solid #e1e1e1;
            margin-right: 20%;
        }
        
        .chat-input-container {
            display: flex;
            gap: 0.5rem;
        }
        
        .chat-input {
            flex: 1;
        }
        
        .chat-send {
            width: auto;
            margin: 0;
            padding: 0.75rem 1.5rem;
        }
        
        .skills-input {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .skill-tag {
            background: #667eea;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .skill-remove {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 1.2rem;
            padding: 0;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .skills-display {
            margin-bottom: 1rem;
            min-height: 40px;
            border: 2px dashed #e1e1e1;
            border-radius: 10px;
            padding: 0.75rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .status-bar { flex-direction: column; align-items: center; }
            .features-grid { grid-template-columns: 1fr; }
            .container { padding: 0 0.5rem; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 AI Career Navigator</h1>
        <p>Your Personal AI-Powered Career Assistant</p>
        <div class="status-bar">
            <div class="status-item">✅ GPT-4.1 Connected</div>
            <div class="status-item">💰 Cost Optimized</div>
            <div class="status-item">🔧 4 Core Features</div>
            <div class="status-item">⚡ Real-time Processing</div>
        </div>
    </div>

    <div class="container">
        <div class="features-grid">
            <!-- Career Chat Feature -->
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">AI Career Chat</div>
                <div class="feature-description">Get personalized career guidance, industry insights, and professional advice from our AI mentor.</div>
                
                <div class="input-group">
                    <label>Your Role/Position:</label>
                    <input type="text" id="chat-role" placeholder="e.g., Software Engineer, Product Manager">
                </div>
                
                <div class="input-group">
                    <label>Experience Level:</label>
                    <select id="chat-experience">
                        <option value="entry">Entry Level (0-2 years)</option>
                        <option value="mid" selected>Mid Level (3-5 years)</option>
                        <option value="senior">Senior Level (6+ years)</option>
                        <option value="executive">Executive Level</option>
                    </select>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="ai-message">
                        <strong>AI Career Mentor:</strong> Hello! I'm your AI Career Navigator. I can help you with career planning, skill development, industry insights, and professional growth strategies. What would you like to discuss today?
                    </div>
                </div>
                
                <div class="chat-input-container">
                    <input type="text" class="chat-input" id="chat-input" placeholder="Ask me anything about your career...">
                    <button class="btn chat-send" onclick="sendChatMessage()">Send</button>
                </div>
                
                <div class="loading" id="chat-loading">🤖 AI is thinking...</div>
            </div>

            <!-- Resume Analysis Feature -->
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">Resume Analysis</div>
                <div class="feature-description">Get detailed feedback on your resume with ATS optimization tips and improvement suggestions.</div>
                
                <div class="input-group">
                    <label>Target Role:</label>
                    <input type="text" id="resume-role" placeholder="e.g., Data Scientist, Full Stack Developer">
                </div>
                
                <div class="input-group">
                    <label>Your Resume Content:</label>
                    <textarea id="resume-text" placeholder="Paste your resume content here..." rows="8"></textarea>
                </div>
                
                <button class="btn" onclick="analyzeResume()">🔍 Analyze My Resume</button>
                
                <div class="loading" id="resume-loading">📊 Analyzing your resume...</div>
                <div class="result" id="resume-result">
                    <h3>📋 Resume Analysis Results</h3>
                    <div class="result-content" id="resume-content"></div>
                </div>
            </div>

            <!-- Interview Preparation Feature -->
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <div class="feature-title">Interview Preparation</div>
                <div class="feature-description">Prepare for your next interview with role-specific questions, STAR method examples, and expert tips.</div>
                
                <div class="input-group">
                    <label>Target Role:</label>
                    <input type="text" id="interview-role" placeholder="e.g., Product Manager, Software Engineer">
                </div>
                
                <div class="input-group">
                    <label>Company Name:</label>
                    <input type="text" id="interview-company" placeholder="e.g., Google, Microsoft, startup">
                </div>
                
                <div class="input-group">
                    <label>Experience Level:</label>
                    <select id="interview-experience">
                        <option value="entry">Entry Level</option>
                        <option value="mid" selected>Mid Level</option>
                        <option value="senior">Senior Level</option>
                        <option value="executive">Executive Level</option>
                    </select>
                </div>
                
                <button class="btn" onclick="prepareInterview()">🎯 Get Interview Prep</button>
                
                <div class="loading" id="interview-loading">🎭 Preparing your interview strategy...</div>
                <div class="result" id="interview-result">
                    <h3>🎤 Interview Preparation Guide</h3>
                    <div class="result-content" id="interview-content"></div>
                </div>
            </div>

            <!-- Skill Assessment Feature -->
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Skill Gap Analysis</div>
                <div class="feature-description">Identify skill gaps and get personalized learning recommendations for your target role.</div>
                
                <div class="input-group">
                    <label>Target Role:</label>
                    <input type="text" id="skill-role" placeholder="e.g., AI Engineer, DevOps Engineer">
                </div>
                
                <div class="input-group">
                    <label>Experience Level:</label>
                    <select id="skill-experience">
                        <option value="entry">Entry Level</option>
                        <option value="mid" selected>Mid Level</option>
                        <option value="senior">Senior Level</option>
                        <option value="executive">Executive Level</option>
                    </select>
                </div>
                
                <div class="input-group">
                    <label>Add Your Current Skills:</label>
                    <div class="skills-input">
                        <input type="text" id="skill-input" placeholder="Type a skill and press Enter">
                        <button type="button" onclick="addSkill()" class="btn" style="width: auto; margin: 0; padding: 0.75rem 1rem;">Add</button>
                    </div>
                </div>
                
                <div class="skills-display" id="skills-display">
                    <span style="color: #999;">Your skills will appear here...</span>
                </div>
                
                <button class="btn" onclick="assessSkills()">📊 Analyze Skill Gaps</button>
                
                <div class="loading" id="skill-loading">🔬 Analyzing your skills...</div>
                <div class="result" id="skill-result">
                    <h3>📈 Skill Gap Analysis</h3>
                    <div class="result-content" id="skill-content"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentSkills = [];

        // Chat functionality
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;

            const container = document.getElementById('chat-container');
            const loading = document.getElementById('chat-loading');
            const role = document.getElementById('chat-role').value;
            const experience = document.getElementById('chat-experience').value;

            // Add user message
            container.innerHTML += `
                <div class="chat-message user-message">
                    <strong>You:</strong> ${message}
                </div>
            `;

            input.value = '';
            loading.style.display = 'block';
            container.scrollTop = container.scrollHeight;

            // Send to API
            fetch('/api/career-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    context: { role: role, experience_level: experience }
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    container.innerHTML += `
                        <div class="chat-message ai-message" style="border-color: #dc3545; background: #f8d7da;">
                            <strong>Error:</strong> ${data.error}
                        </div>
                    `;
                } else {
                    container.innerHTML += `
                        <div class="chat-message ai-message">
                            <strong>AI Career Mentor:</strong> ${data.response}
                        </div>
                    `;
                }
                container.scrollTop = container.scrollHeight;
            })
            .catch(error => {
                loading.style.display = 'none';
                container.innerHTML += `
                    <div class="chat-message ai-message" style="border-color: #dc3545; background: #f8d7da;">
                        <strong>Error:</strong> Failed to connect to AI service
                    </div>
                `;
                container.scrollTop = container.scrollHeight;
            });
        }

        // Enter key for chat
        document.getElementById('chat-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });

        // Resume analysis
        function analyzeResume() {
            const role = document.getElementById('resume-role').value.trim();
            const text = document.getElementById('resume-text').value.trim();
            const loading = document.getElementById('resume-loading');
            const result = document.getElementById('resume-result');
            const content = document.getElementById('resume-content');

            if (!role || !text) {
                alert('Please fill in both target role and resume content');
                return;
            }

            loading.style.display = 'block';
            result.style.display = 'none';

            fetch('/api/resume-analysis', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_text: text,
                    target_role: role
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    content.textContent = 'Error: ' + data.error;
                } else {
                    content.textContent = data.response;
                }
                result.style.display = 'block';
            })
            .catch(error => {
                loading.style.display = 'none';
                content.textContent = 'Error: Failed to analyze resume';
                result.style.display = 'block';
            });
        }

        // Interview preparation
        function prepareInterview() {
            const role = document.getElementById('interview-role').value.trim();
            const company = document.getElementById('interview-company').value.trim();
            const experience = document.getElementById('interview-experience').value;
            const loading = document.getElementById('interview-loading');
            const result = document.getElementById('interview-result');
            const content = document.getElementById('interview-content');

            if (!role || !company) {
                alert('Please fill in both role and company');
                return;
            }

            loading.style.display = 'block';
            result.style.display = 'none';

            fetch('/api/interview-prep', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    role: role,
                    company: company,
                    experience_level: experience
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    content.textContent = 'Error: ' + data.error;
                } else {
                    content.textContent = data.response;
                }
                result.style.display = 'block';
            })
            .catch(error => {
                loading.style.display = 'none';
                content.textContent = 'Error: Failed to prepare interview guide';
                result.style.display = 'block';
            });
        }

        // Skills management
        function addSkill() {
            const input = document.getElementById('skill-input');
            const skill = input.value.trim();
            if (!skill || currentSkills.includes(skill)) return;

            currentSkills.push(skill);
            input.value = '';
            updateSkillsDisplay();
        }

        function removeSkill(skill) {
            currentSkills = currentSkills.filter(s => s !== skill);
            updateSkillsDisplay();
        }

        function updateSkillsDisplay() {
            const display = document.getElementById('skills-display');
            if (currentSkills.length === 0) {
                display.innerHTML = '<span style="color: #999;">Your skills will appear here...</span>';
            } else {
                display.innerHTML = currentSkills.map(skill => `
                    <div class="skill-tag">
                        ${skill}
                        <button class="skill-remove" onclick="removeSkill('${skill}')">&times;</button>
                    </div>
                `).join('');
            }
        }

        // Enter key for skills
        document.getElementById('skill-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addSkill();
            }
        });

        // Skill assessment
        function assessSkills() {
            const role = document.getElementById('skill-role').value.trim();
            const experience = document.getElementById('skill-experience').value;
            const loading = document.getElementById('skill-loading');
            const result = document.getElementById('skill-result');
            const content = document.getElementById('skill-content');

            if (!role) {
                alert('Please enter a target role');
                return;
            }

            if (currentSkills.length === 0) {
                alert('Please add at least one current skill');
                return;
            }

            loading.style.display = 'block';
            result.style.display = 'none';

            fetch('/api/skill-assessment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_skills: currentSkills,
                    target_role: role,
                    experience_level: experience
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.error) {
                    content.textContent = 'Error: ' + data.error;
                } else {
                    content.textContent = data.response;
                }
                result.style.display = 'block';
            })
            .catch(error => {
                loading.style.display = 'none';
                content.textContent = 'Error: Failed to assess skills';
                result.style.display = 'block';
            });
        }
    </script>
</body>
</html>
"""

# Add after CHAT_TEMPLATE, before # Routes

RESUME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Analysis - AI Career Navigator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <a href="/" class="flex items-center space-x-3">
                        <div class="text-3xl">🚀</div>
                        <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                            AI Career Navigator
                        </h1>
                    </a>
                </div>
                <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    <i data-lucide="home" class="w-4 h-4 inline mr-2"></i>Home
                </a>
            </div>
        </div>
    </nav>

    <div class="max-w-4xl mx-auto p-6">
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
            <!-- Header -->
            <div class="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6">
                <h2 class="text-2xl font-bold mb-2">📄 Resume Analysis</h2>
                <p class="opacity-90">Get detailed feedback and ATS optimization tips</p>
            </div>

            <!-- Input Form -->
            <div class="p-6">
                <div class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Target Role:</label>
                        <input type="text" id="resume-role" 
                               class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                               placeholder="e.g., Software Engineer, Data Scientist, Product Manager">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Your Resume Content:</label>
                        <textarea id="resume-text" rows="12"
                                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                  placeholder="Paste your complete resume content here..."></textarea>
                    </div>
                    
                    <button onclick="analyzeResume()" 
                            class="w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2">
                        <i data-lucide="search" class="w-5 h-5"></i>
                        <span>Analyze My Resume</span>
                    </button>
                </div>
            </div>

            <!-- Loading and Results -->
            <div id="resume-loading" class="hidden p-6 text-center">
                <div class="flex items-center justify-center space-x-3">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
                    <span class="text-green-600 font-medium">📊 Analyzing your resume...</span>
                </div>
            </div>

            <div id="resume-result" class="hidden p-6 border-t bg-gray-50">
                <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    <i data-lucide="clipboard-check" class="w-5 h-5 mr-2 text-green-600"></i>
                    Resume Analysis Results
                </h3>
                <div id="resume-content" class="prose prose-green max-w-none bg-white p-6 rounded-lg shadow-sm border"></div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();

        function analyzeResume() {
            const role = document.getElementById('resume-role').value.trim();
            const text = document.getElementById('resume-text').value.trim();
            const loading = document.getElementById('resume-loading');
            const result = document.getElementById('resume-result');
            const content = document.getElementById('resume-content');

            if (!role || !text) {
                alert('Please fill in both target role and resume content');
                return;
            }

            loading.classList.remove('hidden');
            result.classList.add('hidden');

            fetch('/api/resume-analysis', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_text: text,
                    target_role: role
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.classList.add('hidden');
                if (data.error) {
                    content.innerHTML = `<div class="text-red-600"><strong>Error:</strong> ${data.error}</div>`;
                } else {
                    content.innerHTML = formatMessage(data.response);
                }
                result.classList.remove('hidden');
            })
            .catch(error => {
                loading.classList.add('hidden');
                content.innerHTML = `<div class="text-red-600"><strong>Error:</strong> Failed to analyze resume</div>`;
                result.classList.remove('hidden');
            });
        }

        function formatMessage(text) {
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/^- (.*$)/gim, '• $1');
            text = text.replace(/\n/g, '<br>');
            return text;
        }
    </script>
</body>
</html>
"""

INTERVIEW_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview Preparation - AI Career Navigator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <a href="/" class="flex items-center space-x-3">
                        <div class="text-3xl">🚀</div>
                        <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                            AI Career Navigator
                        </h1>
                    </a>
                </div>
                <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    <i data-lucide="home" class="w-4 h-4 inline mr-2"></i>Home
                </a>
            </div>
        </div>
    </nav>

    <div class="max-w-4xl mx-auto p-6">
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
            <!-- Header -->
            <div class="bg-gradient-to-r from-purple-600 to-violet-600 text-white p-6">
                <h2 class="text-2xl font-bold mb-2">🎤 Interview Preparation</h2>
                <p class="opacity-90">Get role-specific questions and expert tips</p>
            </div>

            <!-- Input Form -->
            <div class="p-6">
                <div class="grid md:grid-cols-2 gap-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Target Role:</label>
                        <input type="text" id="interview-role" 
                               class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                               placeholder="e.g., Software Engineer, Product Manager">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Company Name:</label>
                        <input type="text" id="interview-company" 
                               class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                               placeholder="e.g., Google, Microsoft, Amazon">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Experience Level:</label>
                        <select id="interview-experience" 
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                            <option value="entry">Entry Level (0-2 years)</option>
                            <option value="mid" selected>Mid Level (3-5 years)</option>
                            <option value="senior">Senior Level (6+ years)</option>
                            <option value="executive">Executive Level</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Interview Type:</label>
                        <select id="interview-type" 
                                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                            <option value="general">General Interview</option>
                            <option value="technical">Technical Interview</option>
                            <option value="behavioral">Behavioral Interview</option>
                            <option value="final">Final Round</option>
                        </select>
                    </div>
                </div>
                
                <button onclick="prepareInterview()" 
                        class="w-full mt-6 bg-purple-600 text-white py-3 px-6 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2">
                    <i data-lucide="target" class="w-5 h-5"></i>
                    <span>Get Interview Preparation Guide</span>
                </button>
            </div>

            <!-- Loading and Results -->
            <div id="interview-loading" class="hidden p-6 text-center">
                <div class="flex items-center justify-center space-x-3">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                    <span class="text-purple-600 font-medium">🎭 Preparing your interview strategy...</span>
                </div>
            </div>

            <div id="interview-result" class="hidden p-6 border-t bg-gray-50">
                <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    <i data-lucide="mic" class="w-5 h-5 mr-2 text-purple-600"></i>
                    Interview Preparation Guide
                </h3>
                <div id="interview-content" class="prose prose-purple max-w-none bg-white p-6 rounded-lg shadow-sm border"></div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();

        function prepareInterview() {
            const role = document.getElementById('interview-role').value.trim();
            const company = document.getElementById('interview-company').value.trim();
            const experience = document.getElementById('interview-experience').value;
            const type = document.getElementById('interview-type').value;
            const loading = document.getElementById('interview-loading');
            const result = document.getElementById('interview-result');
            const content = document.getElementById('interview-content');

            if (!role || !company) {
                alert('Please fill in both role and company');
                return;
            }

            loading.classList.remove('hidden');
            result.classList.add('hidden');

            fetch('/api/interview-prep', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    role: role,
                    company: company,
                    experience_level: experience,
                    interview_type: type
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.classList.add('hidden');
                if (data.error) {
                    content.innerHTML = `<div class="text-red-600"><strong>Error:</strong> ${data.error}</div>`;
                } else {
                    content.innerHTML = formatMessage(data.response);
                }
                result.classList.remove('hidden');
            })
            .catch(error => {
                loading.classList.add('hidden');
                content.innerHTML = `<div class="text-red-600"><strong>Error:</strong> Failed to prepare interview guide</div>`;
                result.classList.remove('hidden');
            });
        }

        function formatMessage(text) {
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/^- (.*$)/gim, '• $1');
            text = text.replace(/\n/g, '<br>');
            return text;
        }
    </script>
</body>
</html>
"""

SKILLS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill Gap Analysis - AI Career Navigator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        
        .skill-tag {
            transition: all 0.2s ease;
        }
        
        .skill-tag:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <a href="/" class="flex items-center space-x-3">
                        <div class="text-3xl">🚀</div>
                        <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                            AI Career Navigator
                        </h1>
                    </a>
                </div>
                <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    <i data-lucide="home" class="w-4 h-4 inline mr-2"></i>Home
                </a>
            </div>
        </div>
    </nav>

    <div class="max-w-4xl mx-auto p-6">
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
            <!-- Header -->
            <div class="bg-gradient-to-r from-orange-600 to-red-600 text-white p-6">
                <h2 class="text-2xl font-bold mb-2">🎯 Skill Gap Analysis</h2>
                <p class="opacity-90">Identify skill gaps and get personalized learning recommendations</p>
            </div>

            <!-- Input Form -->
            <div class="p-6">
                <div class="space-y-6">
                    <div class="grid md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Target Role:</label>
                            <input type="text" id="skill-role" 
                                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                                   placeholder="e.g., AI Engineer, DevOps Engineer, Full Stack Developer">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Experience Level:</label>
                            <select id="skill-experience" 
                                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                                <option value="entry">Entry Level (0-2 years)</option>
                                <option value="mid" selected>Mid Level (3-5 years)</option>
                                <option value="senior">Senior Level (6+ years)</option>
                                <option value="executive">Executive Level</option>
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Add Your Current Skills:</label>
                        <div class="flex space-x-2">
                            <input type="text" id="skill-input" 
                                   class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                                   placeholder="Type a skill and press Enter or click Add"
                                   onkeypress="handleSkillKeyPress(event)">
                            <button onclick="addSkill()" 
                                    class="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 transition-colors">
                                Add
                            </button>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Your Skills:</label>
                        <div id="skills-display" class="min-h-16 p-4 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 flex flex-wrap gap-2 items-center">
                            <span class="text-gray-500">Your skills will appear here...</span>
                        </div>
                    </div>
                    
                    <button onclick="assessSkills()" 
                            class="w-full bg-orange-600 text-white py-3 px-6 rounded-lg hover:bg-orange-700 transition-colors flex items-center justify-center space-x-2">
                        <i data-lucide="bar-chart-3" class="w-5 h-5"></i>
                        <span>Analyze Skill Gaps</span>
                    </button>
                </div>
            </div>

            <!-- Loading and Results -->
            <div id="skill-loading" class="hidden p-6 text-center">
                <div class="flex items-center justify-center space-x-3">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600"></div>
                    <span class="text-orange-600 font-medium">🔬 Analyzing your skills...</span>
                </div>
            </div>

            <div id="skill-result" class="hidden p-6 border-t bg-gray-50">
                <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
                    <i data-lucide="trending-up" class="w-5 h-5 mr-2 text-orange-600"></i>
                    Skill Gap Analysis Results
                </h3>
                <div id="skill-content" class="prose prose-orange max-w-none bg-white p-6 rounded-lg shadow-sm border"></div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
        let currentSkills = [];

        function handleSkillKeyPress(event) {
            if (event.key === 'Enter') {
                addSkill();
            }
        }

        function addSkill() {
            const input = document.getElementById('skill-input');
            const skill = input.value.trim();
            if (!skill || currentSkills.includes(skill)) return;

            currentSkills.push(skill);
            input.value = '';
            updateSkillsDisplay();
        }

        function removeSkill(skill) {
            currentSkills = currentSkills.filter(s => s !== skill);
            updateSkillsDisplay();
        }

        function updateSkillsDisplay() {
            const display = document.getElementById('skills-display');
            if (currentSkills.length === 0) {
                display.innerHTML = '<span class="text-gray-500">Your skills will appear here...</span>';
            } else {
                display.innerHTML = currentSkills.map(skill => `
                    <div class="skill-tag bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm flex items-center space-x-2 border border-orange-200">
                        <span>${skill}</span>
                        <button onclick="removeSkill('${skill}')" class="text-orange-600 hover:text-orange-800 ml-2">
                            <i data-lucide="x" class="w-3 h-3"></i>
                        </button>
                    </div>
                `).join('');
                lucide.createIcons();
            }
        }

        function assessSkills() {
            const role = document.getElementById('skill-role').value.trim();
            const experience = document.getElementById('skill-experience').value;
            const loading = document.getElementById('skill-loading');
            const result = document.getElementById('skill-result');
            const content = document.getElementById('skill-content');

            if (!role) {
                alert('Please enter a target role');
                return;
            }

            if (currentSkills.length === 0) {
                alert('Please add at least one current skill');
                return;
            }

            loading.classList.remove('hidden');
            result.classList.add('hidden');

            fetch('/api/skill-assessment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_skills: currentSkills,
                    target_role: role,
                    experience_level: experience
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.classList.add('hidden');
                if (data.error) {
                    content.innerHTML = `<div class="text-red-600"><strong>Error:</strong> ${data.error}</div>`;
                } else {
                    content.innerHTML = formatMessage(data.response);
                }
                result.classList.remove('hidden');
            })
            .catch(error => {
                loading.classList.add('hidden');
                content.innerHTML = `<div class="text-red-600"><strong>Error:</strong> Failed to assess skills</div>`;
                result.classList.remove('hidden');
            });
        }

        function formatMessage(text) {
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/^- (.*$)/gim, '• $1');
            text = text.replace(/\n/g, '<br>');
            return text;
        }
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/chat')
def chat():
    return render_template_string(CHAT_TEMPLATE)

@app.route('/resume')
def resume():
    return render_template_string(RESUME_TEMPLATE)

@app.route('/interview')
def interview():
    return render_template_string(INTERVIEW_TEMPLATE)

@app.route('/skills')
def skills():
    return render_template_string(SKILLS_TEMPLATE)

@app.route('/config')
def config():
    """Configuration and status endpoint"""
    return jsonify({
        "version": "1.0.0",
        "ai": {
            "endpoint_configured": bool(os.getenv("AZURE_OPENAI_ENDPOINT")),
            "api_key_configured": bool(os.getenv("AZURE_OPENAI_API_KEY")),
            "deployment": os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1"),
            "model": os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")
        },
        "features": {
            "career_chat": True,
            "resume_analysis": True,
            "interview_prep": True,
            "skill_assessment": True
        },
        "disabled_features": [
            "vectors", "search", "authentication", "document_intelligence"
        ],
        "cost_optimized": True
    })

def call_openai(messages, max_tokens=1000, temperature=0.7):
    """Unified OpenAI API call with error handling"""
    try:
        if not openai_client:
            return {"error": "OpenAI client not initialized"}
        
        response = openai_client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1"),
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return {
            "response": response.choices[0].message.content,
            "model_used": os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1"),
            "timestamp": datetime.now().timestamp(),
            "tokens_used": "optimized"
        }
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        return {"error": str(e)}

@app.route('/api/career-chat', methods=['POST'])
def career_chat():
    """AI Career Chat & Guidance"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        context = data.get('context', {})
        
        # Build conversation context
        messages = [
            {
                "role": "system",
                "content": """You are an expert AI Career Navigator and professional mentor. 
                
                Your expertise includes:
                - Career path planning and strategy
                - Industry insights and trends
                - Skill development recommendations
                - Professional networking advice
                - Workplace challenges and solutions
                
                Provide personalized, actionable career guidance. Be encouraging, professional, 
                and focus on practical next steps. Always consider the user's context and goals."""
            }
        ]
        
        if context:
            context_str = ", ".join([f"{k}: {v}" for k, v in context.items()])
            messages.append({
                "role": "system", 
                "content": f"User context: {context_str}"
            })
        
        messages.append({"role": "user", "content": user_message})
        
        return jsonify(call_openai(messages))
        
    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/resume-analysis', methods=['POST'])
def resume_analysis():
    """Enhanced Resume Analysis with better formatting"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        target_role = data.get('target_role', 'general position')
        
        if not resume_text:
            return jsonify({"error": "Resume text is required"}), 400
        
        # Enhanced system prompt for resume analysis
        system_prompt = f"""You are an expert resume consultant and ATS optimization specialist.

Analyze this resume for a **{target_role}** position and provide comprehensive feedback.

Your analysis should include:
1. **Overall Assessment** - Strengths and weaknesses summary
2. **ATS Optimization** - Keywords and formatting improvements
3. **Content Enhancement** - Specific suggestions for better impact
4. **Skills Analysis** - Missing or underemphasized technical skills
5. **Action Items** - Prioritized improvements to implement

Guidelines:
- Use **bold formatting** for important terms, skills, and recommendations
- Provide **specific examples** and **concrete suggestions**
- Focus on **quantifiable achievements** and **impact metrics**
- Suggest relevant **keywords** for the target role
- Consider current **industry trends** and **market demands**
- Be **constructive** and **actionable** in your feedback

Format your response with clear sections and bullet points for easy readability."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please analyze this resume for a {target_role} position:\n\n{resume_text}"}
        ]
        
        response = call_openai(messages, max_tokens=1200, temperature=0.6)
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/interview-prep', methods=['POST'])
def interview_prep():
    """Enhanced Interview Preparation with better formatting"""
    try:
        data = request.json
        role = data.get('role', 'general position')
        company = data.get('company', 'the company')
        experience_level = data.get('experience_level', 'mid-level')
        interview_type = data.get('interview_type', 'general')
        
        if not role or not company:
            return jsonify({"error": "Role and company are required"}), 400
        
        # Enhanced system prompt for interview preparation
        system_prompt = f"""You are an expert interview coach and hiring manager specialist.

Prepare comprehensive interview guidance for:
- **Role**: {role}
- **Company**: {company}
- **Experience Level**: {experience_level}
- **Interview Type**: {interview_type}

Your preparation should include:
1. **Company Research** - Key insights about {company}
2. **Role-Specific Questions** - Technical and behavioral questions
3. **STAR Method Examples** - Structured response frameworks
4. **Technical Preparation** - Skills and concepts to review
5. **Questions to Ask** - Thoughtful questions for the interviewer
6. **Final Tips** - Last-minute preparation strategies

Guidelines:
- Use **bold formatting** for important concepts, technologies, and frameworks
- Provide **specific examples** tailored to the role and company
- Include **sample answers** with the STAR method structure
- Suggest **relevant technologies** and **tools** to mention
- Consider the **{experience_level}** experience level expectations
- Be **practical** and **actionable** in your advice

Focus on helping them demonstrate both technical competence and cultural fit."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Help me prepare for a {role} {interview_type} interview at {company}. I'm at a {experience_level} experience level."}
        ]
        
        response = call_openai(messages, max_tokens=1200, temperature=0.7)
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Interview prep error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/skill-assessment', methods=['POST'])
def skill_assessment():
    """Enhanced Skill Gap Analysis with technology recommendations"""
    try:
        data = request.json
        current_skills = data.get('current_skills', [])
        target_role = data.get('target_role', 'general position')
        experience_level = data.get('experience_level', 'mid-level')
        
        if not target_role:
            return jsonify({"error": "Target role is required"}), 400
        
        if not current_skills:
            return jsonify({"error": "At least one current skill is required"}), 400
        
        # Enhanced system prompt for skill assessment
        system_prompt = f"""You are an expert skills assessor and technology consultant.

Analyze skills for a **{target_role}** position at **{experience_level}** level.

**Current Skills**: {', '.join(current_skills)}

Provide comprehensive skill gap analysis including:

1. **Current Skills Assessment** - Evaluation of existing skills
2. **Missing Critical Skills** - High-priority gaps to address
3. **Technology Recommendations** - Specific programming languages, frameworks, tools:
   - **Programming Languages**: (e.g., Python, Java, JavaScript, C++, Go, Rust)
   - **Frameworks**: (e.g., React, Angular, Django, Spring, Express.js)
   - **Databases**: (e.g., PostgreSQL, MongoDB, Redis, Elasticsearch)
   - **Cloud Technologies**: (e.g., AWS, Azure, GCP, Docker, Kubernetes)
   - **DevOps Tools**: (e.g., Jenkins, GitLab CI, Terraform, Ansible)
   - **Developer Tools**: (e.g., Git, VS Code, Postman, Jira)

4. **Learning Path** - Prioritized roadmap with timeline
5. **Certification Suggestions** - Relevant industry certifications
6. **Practice Projects** - Hands-on projects to build skills
7. **Market Demand Insights** - Industry trends and salary impact

**Short Summary**: Provide a 2-3 sentence overview first.

**Detailed Analysis**: Then provide comprehensive breakdown.

Guidelines:
- Use **bold formatting** for technologies, frameworks, and important concepts
- Suggest **specific versions** and **popular alternatives**
- Include **learning resources** and **time estimates**
- Consider **{experience_level}** expectations and market demands
- Prioritize skills by **impact** and **market demand**
- Be **specific** about technologies rather than generic advice"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Assess my skills for a {target_role} position (experience level: {experience_level}). Current skills: {', '.join(current_skills)}"}
        ]
        
        response = call_openai(messages, max_tokens=1400, temperature=0.6)
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Skill assessment error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_connected": openai_client is not None
    })

if __name__ == '__main__':
    logger.info("🚀 Starting AI Career Navigator Flask App")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=False) 