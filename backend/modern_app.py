"""
AI Career Navigator - Modern UI inspired by ReactBits.dev
Professional career guidance platform powered by Azure OpenAI GPT-4.1
Created with love by Aryan Jaiswal
"""

import os
import logging
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from openai import AzureOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Azure OpenAI client
try:
    azure_openai_client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://gpt-31.openai.azure.com/"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    )
    logger.info("✅ Azure OpenAI client initialized")
    logger.info(f"📍 Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logger.info(f"🤖 Model: {os.getenv('AZURE_OPENAI_CHATGPT_MODEL', 'gpt-4.1')}")
except Exception as e:
    logger.error(f"❌ Failed to initialize Azure OpenAI: {e}")
    azure_openai_client = None

# Modern UI Templates inspired by ReactBits.dev
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Career Navigator - Modern Career Guidance Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        body { 
            font-family: 'Inter', sans-serif; 
        }
        
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }
        
        .glassmorphism {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .bento-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        .bento-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        }
        
        .floating-animation {
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-20px) rotate(1deg); }
            66% { transform: translateY(-10px) rotate(-1deg); }
        }
        
        .glow-effect {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }
            to { box-shadow: 0 0 30px rgba(102, 126, 234, 0.6); }
        }
        
        .text-gradient {
            background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .feature-icon {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .pulse-ring {
            animation: pulse-ring 2s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite;
        }
        
        @keyframes pulse-ring {
            0% { transform: scale(.33); }
            80%, 100% { opacity: 0; }
        }
        
        .grid-background {
            background-image: 
                linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
        }
    </style>
</head>
<body class="bg-gray-50 overflow-x-hidden">
    <!-- Navigation with glassmorphism -->
    <nav class="fixed top-0 w-full z-50 glassmorphism">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-4">
                    <div class="floating-animation text-3xl">🚀</div>
                    <h1 class="text-xl font-bold text-gradient">
                        AI Career Navigator
                    </h1>
                </div>
                <div class="hidden md:flex items-center space-x-6">
                    <a href="#features" class="text-white/80 hover:text-white transition-all duration-300 font-medium">Features</a>
                    <a href="#about" class="text-white/80 hover:text-white transition-all duration-300 font-medium">About</a>
                    <a href="#contact" class="text-white/80 hover:text-white transition-all duration-300 font-medium">Contact</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section with animated background -->
    <section class="gradient-bg grid-background min-h-screen flex items-center justify-center relative overflow-hidden">
        <!-- Floating elements -->
        <div class="absolute top-20 left-10 w-20 h-20 bg-white/10 rounded-full blur-xl floating-animation"></div>
        <div class="absolute bottom-20 right-10 w-32 h-32 bg-white/10 rounded-full blur-xl floating-animation" style="animation-delay: -3s;"></div>
        
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white relative z-10">
            <div class="floating-animation text-8xl mb-8">🚀</div>
            
            <h1 class="text-5xl md:text-7xl font-black mb-6 leading-tight">
                Your Personal
                <span class="block text-yellow-300 text-gradient">AI Career Coach</span>
            </h1>
            
            <!-- Status badges with glassmorphism -->
            <div class="flex flex-wrap justify-center gap-4 mb-12">
                <div class="glassmorphism px-6 py-3 rounded-full flex items-center space-x-2">
                    <div class="w-2 h-2 bg-green-400 rounded-full pulse-ring"></div>
                    <span class="font-medium">GPT-4.1 Powered</span>
                </div>
                <div class="glassmorphism px-6 py-3 rounded-full flex items-center space-x-2">
                    <div class="w-2 h-2 bg-blue-400 rounded-full pulse-ring"></div>
                    <span class="font-medium">Real-time Analysis</span>
                </div>
                <div class="glassmorphism px-6 py-3 rounded-full flex items-center space-x-2">
                    <div class="w-2 h-2 bg-purple-400 rounded-full pulse-ring"></div>
                    <span class="font-medium">4 Core Features</span>
                </div>
                <div class="glassmorphism px-6 py-3 rounded-full flex items-center space-x-2">
                    <div class="w-2 h-2 bg-yellow-400 rounded-full pulse-ring"></div>
                    <span class="font-medium">Cost Optimized</span>
                </div>
            </div>
            
            <!-- CTA Button with glow effect -->
            <button onclick="document.getElementById('features').scrollIntoView({behavior: 'smooth'})" 
                    class="glow-effect bg-white text-gray-900 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-all duration-300 transform hover:scale-105">
                Explore Features ✨
            </button>
        </div>
    </section>

    <!-- Bento Grid Features Section -->
    <section id="features" class="py-20 bg-gray-50 relative">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-black text-gray-900 mb-6">
                    Powerful Career Tools
                </h2>
                <p class="text-xl text-gray-600 max-w-3xl mx-auto font-light">
                    Everything you need to accelerate your career growth in one intelligent platform
                </p>
            </div>
            
            <!-- Bento Grid Layout -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 auto-rows-fr">
                <!-- AI Career Chat - Large card -->
                <div class="lg:col-span-2 lg:row-span-2 bento-card p-8 rounded-3xl cursor-pointer group"
                     onclick="window.location.href='/chat'">
                    <div class="h-full flex flex-col justify-between">
                        <div>
                            <div class="feature-icon text-6xl mb-6 group-hover:scale-110 transition-transform duration-300">💬</div>
                            <h3 class="text-3xl font-bold text-white mb-4">AI Career Chat</h3>
                            <p class="text-white/80 text-lg leading-relaxed mb-6">
                                Get personalized career guidance, industry insights, and professional advice from our 
                                AI mentor powered by advanced language models.
                            </p>
                        </div>
                        <div class="flex items-center text-white font-semibold group-hover:translate-x-2 transition-transform duration-300">
                            Start Conversation <i data-lucide="arrow-right" class="ml-2 w-5 h-5"></i>
                        </div>
                    </div>
                </div>

                <!-- Resume Analysis -->
                <div class="lg:col-span-1 bento-card p-6 rounded-3xl cursor-pointer group"
                     onclick="window.location.href='/resume'">
                    <div class="feature-icon text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">📄</div>
                    <h3 class="text-xl font-bold text-white mb-3">Resume Analysis</h3>
                    <p class="text-white/80 text-sm leading-relaxed mb-4">
                        ATS optimization tips and improvement suggestions.
                    </p>
                    <div class="flex items-center text-white text-sm font-semibold group-hover:translate-x-1 transition-transform duration-300">
                        Analyze <i data-lucide="arrow-right" class="ml-1 w-4 h-4"></i>
                    </div>
                </div>

                <!-- Interview Prep -->
                <div class="lg:col-span-1 bento-card p-6 rounded-3xl cursor-pointer group"
                     onclick="window.location.href='/interview'">
                    <div class="feature-icon text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">🎤</div>
                    <h3 class="text-xl font-bold text-white mb-3">Interview Prep</h3>
                    <p class="text-white/80 text-sm leading-relaxed mb-4">
                        Role-specific questions and STAR method examples.
                    </p>
                    <div class="flex items-center text-white text-sm font-semibold group-hover:translate-x-1 transition-transform duration-300">
                        Prepare <i data-lucide="arrow-right" class="ml-1 w-4 h-4"></i>
                    </div>
                </div>

                <!-- Skill Gap Analysis - Wide card -->
                <div class="lg:col-span-2 bento-card p-6 rounded-3xl cursor-pointer group"
                     onclick="window.location.href='/skills'">
                    <div class="flex items-center justify-between h-full">
                        <div>
                            <div class="feature-icon text-5xl mb-4 group-hover:scale-110 transition-transform duration-300">🎯</div>
                            <h3 class="text-2xl font-bold text-white mb-3">Skill Gap Analysis</h3>
                            <p class="text-white/80 leading-relaxed mb-4 max-w-md">
                                Identify skill gaps and get personalized learning recommendations with specific 
                                technologies and frameworks.
                            </p>
                            <div class="flex items-center text-white font-semibold group-hover:translate-x-2 transition-transform duration-300">
                                Analyze Skills <i data-lucide="arrow-right" class="ml-2 w-5 h-5"></i>
                            </div>
                        </div>
                        <div class="hidden lg:block text-6xl opacity-20 group-hover:opacity-30 transition-opacity duration-300">📊</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section with modern design -->
    <section id="about" class="py-20 bg-white">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16">
                <h2 class="text-4xl md:text-5xl font-black text-gray-900 mb-6">About This Platform</h2>
            </div>
            
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <div class="space-y-6 text-lg text-gray-600 leading-relaxed">
                        <p>
                            <strong class="text-gray-900">AI Career Navigator</strong> is a cutting-edge career guidance platform built with passion and precision. 
                            Inspired by the need for personalized, intelligent career advice in today's rapidly evolving job market.
                        </p>
                        <p>
                            This platform leverages <strong class="text-gray-900">Azure OpenAI's GPT-4.1</strong> to provide real-time, contextual career guidance. 
                            Built using modern technologies for optimal performance and scalability.
                        </p>
                        <p>
                            The inspiration came from observing how challenging it can be for professionals and students to navigate 
                            career decisions without proper guidance. This platform democratizes access to <strong class="text-gray-900">professional career coaching</strong> 
                            through AI technology.
                        </p>
                    </div>
                </div>
                
                <div class="space-y-4">
                    <div class="glassmorphism p-6 rounded-2xl border border-gray-200">
                        <h3 class="text-xl font-bold text-gray-900 mb-3">Technical Stack</h3>
                        <div class="grid grid-cols-2 gap-4 text-sm">
                            <div><strong>Backend:</strong> Flask, Python, Azure OpenAI</div>
                            <div><strong>Frontend:</strong> Tailwind CSS, Modern JS</div>
                            <div><strong>Deployment:</strong> Azure App Service</div>
                            <div><strong>AI:</strong> GPT-4.1, Cost-Optimized</div>
                        </div>
                    </div>
                    
                    <div class="glassmorphism p-6 rounded-2xl border border-gray-200">
                        <h3 class="text-xl font-bold text-gray-900 mb-3">Design Inspiration</h3>
                        <p class="text-gray-600">
                            UI components inspired by <a href="https://www.reactbits.dev/" target="_blank" class="text-blue-600 hover:text-blue-800 font-semibold">ReactBits.dev</a>, 
                            featuring modern glassmorphism, bento grids, and smooth animations.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer with modern styling -->
    <footer id="contact" class="bg-gray-900 text-white py-16 relative overflow-hidden">
        <!-- Background pattern -->
        <div class="absolute inset-0 grid-background opacity-10"></div>
        
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="text-center">
                <div class="floating-animation text-5xl mb-6">🚀</div>
                <h3 class="text-3xl font-bold mb-4">AI Career Navigator</h3>
                <p class="text-gray-300 mb-8 text-lg">Empowering careers through intelligent technology</p>
                
                <!-- Social links with hover effects -->
                <div class="flex justify-center space-x-6 mb-8">
                    <a href="mailto:aryanjstar3@gmail.com" 
                       class="bg-gray-800 p-3 rounded-full hover:bg-gray-700 transition-all duration-300 hover:scale-110">
                        <i data-lucide="mail" class="w-6 h-6"></i>
                    </a>
                    <a href="#" class="bg-gray-800 p-3 rounded-full hover:bg-gray-700 transition-all duration-300 hover:scale-110">
                        <i data-lucide="github" class="w-6 h-6"></i>
                    </a>
                    <a href="#" class="bg-gray-800 p-3 rounded-full hover:bg-gray-700 transition-all duration-300 hover:scale-110">
                        <i data-lucide="linkedin" class="w-6 h-6"></i>
                    </a>
                </div>
                
                <div class="border-t border-gray-700 pt-8">
                    <p class="text-gray-400 mb-2">
                        Built with <span class="text-red-500 text-xl">❤️</span> by <strong class="text-white">Aryan Jaiswal</strong>
                    </p>
                    <p class="text-gray-500">
                        <a href="mailto:aryanjstar3@gmail.com" class="hover:text-blue-400 transition-colors">
                            aryanjstar3@gmail.com
                        </a>
                    </p>
                    <p class="text-gray-600 text-sm mt-4">
                        Inspired by <a href="https://www.reactbits.dev/" target="_blank" class="text-blue-400 hover:text-blue-300">ReactBits.dev</a> • 
                        Powered by Azure OpenAI GPT-4.1
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Initialize Lucide icons
        lucide.createIcons();
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Add scroll effect to navigation
        window.addEventListener('scroll', () => {
            const nav = document.querySelector('nav');
            if (window.scrollY > 100) {
                nav.style.background = 'rgba(255, 255, 255, 0.95)';
                nav.style.backdropFilter = 'blur(20px)';
            } else {
                nav.style.background = 'rgba(255, 255, 255, 0.25)';
                nav.style.backdropFilter = 'blur(10px)';
            }
        });
        
        // Add intersection observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        // Observe all bento cards
        document.querySelectorAll('.bento-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    </script>
</body>
</html>
"""

CHAT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Career Chat - AI Career Navigator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
        
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .glassmorphism {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .typing-indicator {
            display: none;
        }
        
        .typing-indicator.active {
            display: flex;
        }
        
        .typing-dots {
            animation: typing 1.4s infinite;
        }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        .message-enter {
            animation: messageSlideIn 0.3s ease-out;
        }
        
        @keyframes messageSlideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body class="gradient-bg min-h-screen">
    <!-- Navigation -->
    <nav class="glassmorphism">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-3">
                    <a href="/" class="flex items-center space-x-3">
                        <div class="text-3xl">🚀</div>
                        <h1 class="text-xl font-bold text-white">
                            AI Career Navigator
                        </h1>
                    </a>
                </div>
                <a href="/" class="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors">
                    <i data-lucide="home" class="w-4 h-4 inline mr-2"></i>Home
                </a>
            </div>
        </div>
    </nav>

    <div class="max-w-4xl mx-auto p-6">
        <div class="glassmorphism rounded-3xl overflow-hidden shadow-2xl">
            <!-- Header -->
            <div class="gradient-bg text-white p-8">
                <div class="flex items-center space-x-4">
                    <div class="text-4xl">💬</div>
                    <div>
                        <h2 class="text-3xl font-bold mb-2">AI Career Chat</h2>
                        <p class="opacity-90">Get personalized career guidance from your AI mentor</p>
                    </div>
                </div>
            </div>

            <!-- Configuration -->
            <div class="p-6 bg-white/10 border-b border-white/20">
                <div class="grid md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-white mb-2">Your Role/Position:</label>
                        <input type="text" id="chat-role" 
                               class="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/60 focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                               placeholder="e.g., Software Engineer, Data Scientist">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-white mb-2">Experience Level:</label>
                        <select id="chat-experience" 
                                class="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all">
                            <option value="entry">Entry Level (0-2 years)</option>
                            <option value="mid" selected>Mid Level (3-5 years)</option>
                            <option value="senior">Senior Level (6+ years)</option>
                            <option value="executive">Executive Level</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Chat Container -->
            <div id="chat-container" class="h-96 p-6 space-y-4">
                <div class="flex items-start space-x-3 message-enter">
                    <div class="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        AI
                    </div>
                    <div class="glassmorphism rounded-2xl p-4 max-w-md text-white">
                        <p>
                            Hello! I'm your AI Career Mentor. I'm here to help you with career guidance, 
                            industry insights, and professional advice. What would you like to discuss today?
                        </p>
                    </div>
                </div>
            </div>

            <!-- Typing Indicator -->
            <div class="typing-indicator px-6 pb-4">
                <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        AI
                    </div>
                    <div class="glassmorphism rounded-2xl p-4">
                        <div class="typing-dots flex space-x-1">
                            <div class="w-2 h-2 bg-white/60 rounded-full"></div>
                            <div class="w-2 h-2 bg-white/60 rounded-full"></div>
                            <div class="w-2 h-2 bg-white/60 rounded-full"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input Area -->
            <div class="p-6 border-t border-white/20 bg-white/5">
                <div class="flex space-x-4">
                    <input type="text" id="chat-input" 
                           class="flex-1 px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/60 focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                           placeholder="Ask me about career advice, industry trends, skills development..."
                           onkeypress="handleKeyPress(event)">
                    <button onclick="sendChatMessage()" 
                            class="bg-white text-gray-900 px-6 py-3 rounded-xl hover:bg-gray-100 transition-colors flex items-center font-semibold">
                        <i data-lucide="send" class="w-4 h-4 mr-2"></i>Send
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendChatMessage();
            }
        }

        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;

            const container = document.getElementById('chat-container');
            const typingIndicator = document.querySelector('.typing-indicator');
            const role = document.getElementById('chat-role').value;
            const experience = document.getElementById('chat-experience').value;

            // Add user message with animation
            const userMessage = document.createElement('div');
            userMessage.className = 'flex items-start space-x-3 justify-end message-enter';
            userMessage.innerHTML = `
                <div class="glassmorphism rounded-2xl p-4 max-w-md text-white bg-white/20">
                    <p>${message}</p>
                </div>
                <div class="flex-shrink-0 w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                    You
                </div>
            `;
            container.appendChild(userMessage);

            input.value = '';
            typingIndicator.classList.add('active');
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
                typingIndicator.classList.remove('active');
                const aiMessage = document.createElement('div');
                aiMessage.className = 'flex items-start space-x-3 message-enter';
                
                if (data.error) {
                    aiMessage.innerHTML = `
                        <div class="flex-shrink-0 w-10 h-10 bg-red-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                            !
                        </div>
                        <div class="glassmorphism rounded-2xl p-4 max-w-md bg-red-500/20 border border-red-500/30">
                            <p class="text-white"><strong>Error:</strong> ${data.error}</p>
                        </div>
                    `;
                } else {
                    const formattedResponse = formatMessage(data.response);
                    aiMessage.innerHTML = `
                        <div class="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                            AI
                        </div>
                        <div class="glassmorphism rounded-2xl p-4 max-w-md text-white">
                            <div>${formattedResponse}</div>
                        </div>
                    `;
                }
                
                container.appendChild(aiMessage);
                container.scrollTop = container.scrollHeight;
            })
            .catch(error => {
                typingIndicator.classList.remove('active');
                const errorMessage = document.createElement('div');
                errorMessage.className = 'flex items-start space-x-3 message-enter';
                errorMessage.innerHTML = `
                    <div class="flex-shrink-0 w-10 h-10 bg-red-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        !
                    </div>
                    <div class="glassmorphism rounded-2xl p-4 max-w-md bg-red-500/20 border border-red-500/30">
                        <p class="text-white"><strong>Error:</strong> Failed to connect to AI service</p>
                    </div>
                `;
                container.appendChild(errorMessage);
                container.scrollTop = container.scrollHeight;
            });
        }

        function formatMessage(text) {
            // Format bold text
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
            // Format bullet points
            text = text.replace(/^- (.*$)/gim, '• $1');
            
            // Format line breaks
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

@app.route('/config')
def config():
    """Health check and configuration endpoint"""
    try:
        return jsonify({
            "status": "healthy",
            "version": "3.0.0",
            "features": {
                "ai_chat": True,
                "resume_analysis": True,
                "interview_prep": True,
                "skill_assessment": True
            },
            "ai_service": {
                "provider": "Azure OpenAI",
                "model": os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1"),
                "status": "connected" if azure_openai_client else "disconnected"
            },
            "ui_framework": "ReactBits-inspired Tailwind CSS"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def call_openai(messages, max_tokens=1000, temperature=0.7):
    """Call Azure OpenAI with error handling"""
    try:
        if not azure_openai_client:
            raise Exception("Azure OpenAI client not initialized")
        
        response = azure_openai_client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1"),
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise Exception(f"AI service error: {str(e)}")

@app.route('/api/career-chat', methods=['POST'])
def career_chat():
    """Enhanced AI Career Chat with better formatting"""
    try:
        data = request.json
        user_message = data.get('message', '')
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Enhanced system prompt
        system_prompt = f"""You are an expert AI Career Mentor and professional advisor. 

Context:
- User Role: {context.get('role', 'Not specified')}
- Experience Level: {context.get('experience_level', 'Not specified')}

Guidelines:
1. Provide **personalized**, **actionable** career advice
2. Use **bold formatting** for important terms and concepts
3. Give **specific examples** and **concrete steps**
4. Focus on **practical insights** rather than generic advice
5. Consider current **industry trends** and **market demands**
6. Be **encouraging** and **supportive** while being realistic

Format your response with:
- **Bold** for important concepts, skills, companies, tools
- Clear structure with headers when needed
- Bullet points for lists and action items
- Specific recommendations tailored to their role and experience

Always aim to be helpful, professional, and insightful."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = call_openai(messages, max_tokens=800, temperature=0.7)
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting AI Career Navigator Flask App - ReactBits Inspired")
    app.run(host='0.0.0.0', port=8000, debug=False) 