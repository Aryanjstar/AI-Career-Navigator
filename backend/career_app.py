"""
AI Career Navigator - Professional MERN Stack Platform
Azure OpenAI GPT-4.1 Powered Career Guidance System
Built by Aryan Jaiswal for Internship & Job Applications
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
    
    deployment_name = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1")
    model_name = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")
    
    logger.info(f"✅ Azure OpenAI client initialized")
    logger.info(f"📍 Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logger.info(f"🤖 Model: {model_name}")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize OpenAI client: {e}")
    openai_client = None

# Modern Professional UI Template
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Career Navigator - MERN Stack Platform by Aryan Jaiswal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        body { 
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 25%, #1e40af 50%, #2563eb 75%, #3b82f6 100%);
            min-height: 100vh;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tech-badge {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .active-tab {
            background: rgba(255, 255, 255, 0.2);
            border-bottom: 3px solid #60a5fa;
        }
        
        .chat-message {
            margin-bottom: 16px;
            padding: 12px 16px;
            border-radius: 16px;
            animation: fadeIn 0.3s ease;
        }
        
        .user-message {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            margin-left: 20%;
        }
        
        .ai-message {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid rgba(59, 130, 246, 0.2);
            margin-right: 20%;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .loading-dots {
            display: inline-flex;
            gap: 4px;
        }
        
        .loading-dots div {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #3b82f6;
            animation: loading 1.4s infinite;
        }
        
        .loading-dots div:nth-child(2) { animation-delay: 0.2s; }
        .loading-dots div:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes loading {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="glass-card mx-4 mt-4 px-6 py-4">
        <div class="flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="text-2xl">🚀</div>
                <h1 class="text-xl font-bold text-white">
                    AI Career Navigator
                </h1>
            </div>
            <div class="flex items-center space-x-6">
                <span class="text-white/80 text-sm">MERN Stack Platform</span>
                <div class="tech-badge">GPT-4.1 Powered</div>
            </div>
        </div>
    </nav>

    <!-- Header Section -->
    <div class="text-center py-12 px-4">
        <h1 class="text-5xl md:text-6xl font-black text-white mb-4">
            AI Career Navigator
        </h1>
        <p class="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
            Professional career guidance platform built with MERN Stack & Azure OpenAI GPT-4.1
        </p>
        
        <!-- Tech Stack Showcase -->
        <div class="flex flex-wrap justify-center gap-3 mb-8">
            <div class="tech-badge">MongoDB</div>
            <div class="tech-badge">Express.js</div>
            <div class="tech-badge">React</div>
            <div class="tech-badge">Node.js</div>
            <div class="tech-badge">Azure OpenAI</div>
            <div class="tech-badge">Python</div>
            <div class="tech-badge">Flask</div>
        </div>
    </div>

    <!-- Main Container -->
    <div class="max-w-7xl mx-auto px-4 pb-12">
        <!-- Tab Navigation -->
        <div class="glass-card p-2 mb-8">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <button onclick="switchTab('chat')" id="tab-chat" class="tab-btn px-4 py-3 text-white font-medium rounded-lg transition-all active-tab">
                    💬 Career Chat
                </button>
                <button onclick="switchTab('resume')" id="tab-resume" class="tab-btn px-4 py-3 text-white font-medium rounded-lg transition-all">
                    📄 Resume Analysis
                </button>
                <button onclick="switchTab('interview')" id="tab-interview" class="tab-btn px-4 py-3 text-white font-medium rounded-lg transition-all">
                    🎤 Interview Prep
                </button>
                <button onclick="switchTab('skills')" id="tab-skills" class="tab-btn px-4 py-3 text-white font-medium rounded-lg transition-all">
                    🎯 Skill Analysis
                </button>
            </div>
        </div>

        <!-- Content Sections -->
        <div class="feature-card p-8">
            <!-- Chat Tab -->
            <div id="content-chat" class="tab-content">
                <div class="grid md:grid-cols-3 gap-6 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Your Role:</label>
                        <input type="text" id="chat-role" 
                               class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                               placeholder="e.g., MERN Stack Developer">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Experience:</label>
                        <select id="chat-experience" 
                                class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none">
                            <option value="entry">Entry Level (0-2 years)</option>
                            <option value="mid" selected>Mid Level (3-5 years)</option>
                            <option value="senior">Senior Level (6+ years)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Focus Area:</label>
                        <select id="chat-focus" 
                                class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none">
                            <option value="internship">Internship Search</option>
                            <option value="job">Job Applications</option>
                            <option value="career">Career Growth</option>
                            <option value="skills">Skill Development</option>
                        </select>
                    </div>
                </div>
                
                <div id="chat-container" class="h-80 overflow-y-auto p-4 bg-gray-50 rounded-lg mb-4">
                    <div class="ai-message">
                        <strong>🤖 AI Career Mentor:</strong> Hello! I'm your AI Career Navigator specialized in MERN stack development and tech careers. I can help you with internships, job applications, and career guidance. What would you like to discuss?
                    </div>
                </div>
                
                <div class="flex gap-3">
                    <input type="text" id="chat-input" 
                           class="flex-1 px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                           placeholder="Ask about MERN stack careers, internships, or job applications..."
                           onkeypress="handleChatKeyPress(event)">
                    <button onclick="sendChatMessage()" 
                            class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                        Send
                    </button>
                </div>
                
                <div id="chat-loading" class="hidden text-center py-4">
                    <div class="loading-dots">
                        <div></div><div></div><div></div>
                    </div>
                    <span class="ml-3 text-blue-600">AI is thinking...</span>
                </div>
            </div>

            <!-- Resume Tab -->
            <div id="content-resume" class="tab-content hidden">
                <div class="grid md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Target Role:</label>
                        <input type="text" id="resume-role" 
                               class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                               placeholder="e.g., MERN Stack Developer, Frontend Developer">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Application Type:</label>
                        <select id="resume-type" 
                                class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none">
                            <option value="internship">Internship Application</option>
                            <option value="fulltime">Full-time Job</option>
                            <option value="freelance">Freelance Project</option>
                        </select>
                    </div>
                </div>
                
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Resume Content:</label>
                    <textarea id="resume-text" rows="10"
                              class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                              placeholder="Paste your complete resume content here..."></textarea>
                </div>
                
                <button onclick="analyzeResume()" 
                        class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors mb-4">
                    🔍 Analyze Resume for Tech Roles
                </button>
                
                <div id="resume-loading" class="hidden text-center py-4">
                    <div class="loading-dots">
                        <div></div><div></div><div></div>
                    </div>
                    <span class="ml-3 text-blue-600">Analyzing resume...</span>
                </div>
                
                <div id="resume-result" class="hidden bg-gray-50 p-6 rounded-lg">
                    <h3 class="text-xl font-bold text-gray-900 mb-4">📋 Resume Analysis Results</h3>
                    <div id="resume-content" class="prose max-w-none"></div>
                </div>
            </div>

            <!-- Interview Tab -->
            <div id="content-interview" class="tab-content hidden">
                <div class="grid md:grid-cols-3 gap-6 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Target Role:</label>
                        <input type="text" id="interview-role" 
                               class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                               placeholder="e.g., React Developer, Node.js Engineer">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Company:</label>
                        <input type="text" id="interview-company" 
                               class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                               placeholder="e.g., Google, Microsoft, Startup">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Interview Type:</label>
                        <select id="interview-type" 
                                class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none">
                            <option value="technical">Technical Round</option>
                            <option value="behavioral">Behavioral Round</option>
                            <option value="system-design">System Design</option>
                            <option value="coding">Coding Challenge</option>
                        </select>
                    </div>
                </div>
                
                <button onclick="prepareInterview()" 
                        class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors mb-4">
                    🎯 Get Interview Preparation Guide
                </button>
                
                <div id="interview-loading" class="hidden text-center py-4">
                    <div class="loading-dots">
                        <div></div><div></div><div></div>
                    </div>
                    <span class="ml-3 text-blue-600">Preparing interview guide...</span>
                </div>
                
                <div id="interview-result" class="hidden bg-gray-50 p-6 rounded-lg">
                    <h3 class="text-xl font-bold text-gray-900 mb-4">🎤 Interview Preparation Guide</h3>
                    <div id="interview-content" class="prose max-w-none"></div>
                </div>
            </div>

            <!-- Skills Tab -->
            <div id="content-skills" class="tab-content hidden">
                <div class="grid md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Target Role:</label>
                        <input type="text" id="skill-role" 
                               class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                               placeholder="e.g., Full Stack Developer, DevOps Engineer">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Career Goal:</label>
                        <select id="skill-goal" 
                                class="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none">
                            <option value="internship">Secure Internship</option>
                            <option value="entry-job">Entry Level Job</option>
                            <option value="senior-role">Senior Position</option>
                            <option value="freelance">Freelance Career</option>
                        </select>
                    </div>
                </div>
                
                <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Add Your Current Skills:</label>
                    <div class="flex gap-2 mb-3">
                        <input type="text" id="skill-input" 
                               class="flex-1 px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:outline-none"
                               placeholder="Type a skill and press Enter"
                               onkeypress="handleSkillKeyPress(event)">
                        <button onclick="addSkill()" 
                                class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                            Add
                        </button>
                    </div>
                    
                    <div id="skills-display" class="min-h-20 p-4 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex flex-wrap gap-2">
                        <span class="text-gray-500">Your skills will appear here...</span>
                    </div>
                </div>
                
                <button onclick="assessSkills()" 
                        class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors mb-4">
                    📊 Analyze Skills & Get Learning Path
                </button>
                
                <div id="skill-loading" class="hidden text-center py-4">
                    <div class="loading-dots">
                        <div></div><div></div><div></div>
                    </div>
                    <span class="ml-3 text-blue-600">Analyzing skills...</span>
                </div>
                
                <div id="skill-result" class="hidden bg-gray-50 p-6 rounded-lg">
                    <h3 class="text-xl font-bold text-gray-900 mb-4">📈 Skill Gap Analysis</h3>
                    <div id="skill-content" class="prose max-w-none"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="glass-card mx-4 mb-4 p-8 text-center">
        <div class="text-white">
            <h3 class="text-2xl font-bold mb-4 gradient-text">AI Career Navigator</h3>
            <p class="text-blue-100 mb-6">MERN Stack Career Guidance Platform</p>
            
            <!-- Contact & Links -->
            <div class="flex flex-wrap justify-center items-center gap-6 mb-6">
                <a href="mailto:aryanjstar3@gmail.com" class="flex items-center space-x-2 text-blue-100 hover:text-white transition-colors">
                    <i data-lucide="mail" class="w-5 h-5"></i>
                    <span>aryanjstar3@gmail.com</span>
                </a>
                <a href="https://www.linkedin.com/in/aryanjstar/" target="_blank" class="flex items-center space-x-2 text-blue-100 hover:text-white transition-colors">
                    <i data-lucide="linkedin" class="w-5 h-5"></i>
                    <span>LinkedIn</span>
                </a>
                <a href="https://github.com/Aryanjstar/ai-career-navigator" target="_blank" class="flex items-center space-x-2 text-blue-100 hover:text-white transition-colors">
                    <i data-lucide="github" class="w-5 h-5"></i>
                    <span>GitHub Repository</span>
                </a>
            </div>
            
            <div class="border-t border-white/20 pt-6">
                <p class="text-blue-100 mb-2">
                    Built with <span class="text-red-400">❤️</span> by <strong class="text-white gradient-text">Aryan Jaiswal</strong>
                </p>
                <p class="text-blue-200 text-sm">
                    Powered by Azure OpenAI GPT-4.1 • MERN Stack • Python Flask
                </p>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();
        let currentSkills = [];

        // Tab switching
        function switchTab(tabName) {
            // Hide all content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.add('hidden');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active-tab');
            });
            
            // Show selected content and activate tab
            document.getElementById(`content-${tabName}`).classList.remove('hidden');
            document.getElementById(`tab-${tabName}`).classList.add('active-tab');
        }

        // Chat functionality
        function handleChatKeyPress(event) {
            if (event.key === 'Enter') {
                sendChatMessage();
            }
        }

        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;

            const container = document.getElementById('chat-container');
            const loading = document.getElementById('chat-loading');
            const role = document.getElementById('chat-role').value;
            const experience = document.getElementById('chat-experience').value;
            const focus = document.getElementById('chat-focus').value;

            // Add user message
            const userMessage = document.createElement('div');
            userMessage.className = 'chat-message user-message';
            userMessage.innerHTML = `<strong>You:</strong> ${message}`;
            container.appendChild(userMessage);

            input.value = '';
            loading.classList.remove('hidden');
            container.scrollTop = container.scrollHeight;

            // Send to API
            fetch('/api/career-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    context: { 
                        role: role, 
                        experience_level: experience,
                        focus_area: focus,
                        platform: 'mern_stack'
                    }
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.classList.add('hidden');
                const aiMessage = document.createElement('div');
                aiMessage.className = 'chat-message ai-message';
                
                if (data.error) {
                    aiMessage.innerHTML = `<strong>❌ Error:</strong> ${data.error}`;
                } else {
                    aiMessage.innerHTML = `<strong>🤖 AI Career Mentor:</strong> ${formatMessage(data.response)}`;
                }
                
                container.appendChild(aiMessage);
                container.scrollTop = container.scrollHeight;
            })
            .catch(error => {
                loading.classList.add('hidden');
                const errorMessage = document.createElement('div');
                errorMessage.className = 'chat-message ai-message';
                errorMessage.innerHTML = `<strong>❌ Error:</strong> Failed to connect to AI service`;
                container.appendChild(errorMessage);
                container.scrollTop = container.scrollHeight;
            });
        }

        // Resume analysis
        function analyzeResume() {
            const role = document.getElementById('resume-role').value.trim();
            const text = document.getElementById('resume-text').value.trim();
            const type = document.getElementById('resume-type').value;
            
            if (!role || !text) {
                alert('Please fill in both target role and resume content');
                return;
            }

            const loading = document.getElementById('resume-loading');
            const result = document.getElementById('resume-result');
            const content = document.getElementById('resume-content');

            loading.classList.remove('hidden');
            result.classList.add('hidden');

            fetch('/api/resume-analysis', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_text: text,
                    target_role: role,
                    application_type: type
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

        // Interview preparation
        function prepareInterview() {
            const role = document.getElementById('interview-role').value.trim();
            const company = document.getElementById('interview-company').value.trim();
            const type = document.getElementById('interview-type').value;
            
            if (!role || !company) {
                alert('Please fill in both role and company');
                return;
            }

            const loading = document.getElementById('interview-loading');
            const result = document.getElementById('interview-result');
            const content = document.getElementById('interview-content');

            loading.classList.remove('hidden');
            result.classList.add('hidden');

            fetch('/api/interview-prep', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    role: role,
                    company: company,
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

        // Skills management
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
                    <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm flex items-center space-x-2">
                        <span>${skill}</span>
                        <button onclick="removeSkill('${skill}')" class="text-blue-600 hover:text-blue-800 ml-2">
                            ×
                        </button>
                    </div>
                `).join('');
            }
        }

        // Skill assessment
        function assessSkills() {
            const role = document.getElementById('skill-role').value.trim();
            const goal = document.getElementById('skill-goal').value;
            
            if (!role) {
                alert('Please enter a target role');
                return;
            }

            if (currentSkills.length === 0) {
                alert('Please add at least one current skill');
                return;
            }

            const loading = document.getElementById('skill-loading');
            const result = document.getElementById('skill-result');
            const content = document.getElementById('skill-content');

            loading.classList.remove('hidden');
            result.classList.add('hidden');

            fetch('/api/skill-assessment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_skills: currentSkills,
                    target_role: role,
                    career_goal: goal
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

        // Format messages
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
    return render_template_string(MAIN_TEMPLATE)

@app.route('/config')
def config():
    """Configuration and status endpoint"""
    return jsonify({
        "version": "2.0.0",
        "platform": "MERN Stack Career Navigator",
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
        "tech_stack": ["MongoDB", "Express.js", "React", "Node.js", "Python", "Azure OpenAI"],
        "developer": {
            "name": "Aryan Jaiswal",
            "email": "aryanjstar3@gmail.com",
            "linkedin": "https://www.linkedin.com/in/aryanjstar/",
            "github": "https://github.com/Aryanjstar/ai-career-navigator"
        }
    })

def call_openai(messages, max_tokens=1000, temperature=0.7):
    """Call Azure OpenAI with error handling"""
    try:
        if not openai_client:
            return {"error": "Azure OpenAI client not initialized"}
        
        response = openai_client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1"),
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return {
            "response": response.choices[0].message.content,
            "model_used": os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1"),
            "timestamp": datetime.now().timestamp()
        }
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        return {"error": str(e)}

@app.route('/api/career-chat', methods=['POST'])
def career_chat():
    """MERN Stack focused career chat"""
    try:
        data = request.json
        user_message = data.get('message', '')
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Focused system prompt for MERN stack careers
        system_prompt = f"""You are an expert AI Career Mentor specializing in MERN Stack development and tech careers.

Context:
- User Role: {context.get('role', 'MERN Stack Developer')}
- Experience Level: {context.get('experience_level', 'mid')}
- Focus Area: {context.get('focus_area', 'career')}
- Platform: {context.get('platform', 'mern_stack')}

STRICT GUIDELINES:
1. ONLY answer career-related questions about:
   - MERN Stack (MongoDB, Express.js, React, Node.js) development
   - Web development technologies (JavaScript, TypeScript, HTML, CSS)
   - Tech career advice (internships, jobs, interviews, skills)
   - Software engineering practices
   - Professional development in tech

2. If asked about non-career topics, politely redirect: "I'm specialized in tech career guidance. Please ask about MERN stack development, internships, job applications, or tech skills."

3. Provide **specific**, **actionable** advice with:
   - **Bold formatting** for important technologies and concepts
   - Concrete next steps and resources
   - Focus on practical career advancement
   - Industry-relevant recommendations

4. Emphasize MERN stack skills and related technologies when relevant.

Always be helpful, professional, and focused on career development."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        result = call_openai(messages, max_tokens=800, temperature=0.7)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/resume-analysis', methods=['POST'])
def resume_analysis():
    """Resume analysis for tech roles"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        target_role = data.get('target_role', 'MERN Stack Developer')
        application_type = data.get('application_type', 'internship')
        
        if not resume_text:
            return jsonify({"error": "Resume text is required"}), 400
        
        system_prompt = f"""You are an expert tech resume consultant specializing in MERN stack and web development roles.

Analyze this resume for a **{target_role}** {application_type} position.

ANALYSIS FOCUS:
1. **Technical Skills Assessment** - MERN stack technologies
2. **Project Evaluation** - Web development projects
3. **ATS Optimization** - Keywords for tech roles
4. **Experience Relevance** - Match with target role
5. **Improvement Recommendations** - Specific actionable steps

ONLY provide feedback relevant to:
- MERN Stack development (MongoDB, Express.js, React, Node.js)
- Web technologies (JavaScript, TypeScript, HTML, CSS)
- Related tech skills (Git, AWS, Docker, etc.)
- Software engineering best practices

Format with **bold** for important technologies and clear sections."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this resume for {target_role} {application_type}:\n\n{resume_text}"}
        ]
        
        result = call_openai(messages, max_tokens=1200, temperature=0.6)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/interview-prep', methods=['POST'])
def interview_prep():
    """Interview preparation for tech roles"""
    try:
        data = request.json
        role = data.get('role', 'MERN Stack Developer')
        company = data.get('company', 'tech company')
        interview_type = data.get('interview_type', 'technical')
        
        if not role or not company:
            return jsonify({"error": "Role and company are required"}), 400
        
        system_prompt = f"""You are an expert tech interview coach specializing in MERN stack and web development interviews.

Prepare for: **{role}** {interview_type} interview at **{company}**

PREPARATION AREAS:
1. **Technical Questions** - MERN stack specific
2. **Coding Challenges** - JavaScript/React/Node.js
3. **System Design** - Web application architecture
4. **Behavioral Questions** - Tech team collaboration
5. **Company Research** - {company} tech stack and culture
6. **Questions to Ask** - About tech team and growth

ONLY focus on:
- MERN Stack technologies and concepts
- Web development best practices
- Software engineering principles
- Tech career growth questions

Use **bold** formatting for important concepts and technologies."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Help me prepare for {role} {interview_type} interview at {company}"}
        ]
        
        result = call_openai(messages, max_tokens=1200, temperature=0.7)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Interview prep error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/skill-assessment', methods=['POST'])
def skill_assessment():
    """Skill gap analysis for MERN stack careers"""
    try:
        data = request.json
        current_skills = data.get('current_skills', [])
        target_role = data.get('target_role', 'MERN Stack Developer')
        career_goal = data.get('career_goal', 'internship')
        
        if not target_role or not current_skills:
            return jsonify({"error": "Target role and current skills are required"}), 400
        
        system_prompt = f"""You are an expert tech skills assessor specializing in MERN stack development.

ANALYSIS FOR: **{target_role}** to achieve **{career_goal}**
CURRENT SKILLS: {', '.join(current_skills)}

PROVIDE COMPREHENSIVE ANALYSIS:

1. **Skills Assessment** - Rate current MERN stack proficiency
2. **Critical Gaps** - Missing essential technologies
3. **MERN Stack Roadmap**:
   - **Frontend**: React, JavaScript, TypeScript, HTML, CSS
   - **Backend**: Node.js, Express.js, RESTful APIs
   - **Database**: MongoDB, Mongoose
   - **Tools**: Git, npm/yarn, VS Code, Postman
   - **Cloud**: AWS, Heroku, Netlify
   - **Testing**: Jest, Cypress, Mocha

4. **Learning Path** - Prioritized 3-month plan
5. **Project Recommendations** - Portfolio projects
6. **Certification Suggestions** - Industry-recognized credentials

ONLY focus on web development and MERN stack technologies.
Use **bold** for all technologies and frameworks."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Assess skills for {target_role} ({career_goal}). Current skills: {', '.join(current_skills)}"}
        ]
        
        result = call_openai(messages, max_tokens=1400, temperature=0.6)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Skill assessment error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_connected": openai_client is not None,
        "platform": "MERN Stack Career Navigator",
        "developer": "Aryan Jaiswal"
    })

if __name__ == '__main__':
    logger.info("🚀 Starting AI Career Navigator - MERN Stack Platform")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=False) 