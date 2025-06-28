#!/usr/bin/env python3
import os
import json
import logging
import io
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import openai
from openai import AzureOpenAI
import PyPDF2
from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_CHATGPT_MODEL", "gpt-4.1")

# Initialize Azure OpenAI client
client = None
if AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY:
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version="2024-02-01"
    )
    logger.info("Azure OpenAI client initialized successfully")
else:
    logger.error("Azure OpenAI configuration missing!")

# Beautiful AI Career Navigator Template
CAREER_NAVIGATOR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>AI Career Navigator</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>🚀</text></svg>">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #475569 75%, #64748b 100%);
            min-height: 100vh;
        }
        
        .glass-card {
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.2);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 
                       inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-hover {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-hover:hover {
            background: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 
                       inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }
        
        .floating-rocket {
            animation: float 6s ease-in-out infinite, pulse 2s ease-in-out infinite alternate;
            display: inline-block;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            25% { transform: translateY(-20px) rotate(2deg); }
            50% { transform: translateY(-15px) rotate(0deg); }
            75% { transform: translateY(-25px) rotate(-2deg); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            100% { transform: scale(1.1); }
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #60a5fa, #8b5cf6, #a855f7, #3b82f6);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 4s ease-in-out infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .pulse-glow {
            animation: pulse-glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes pulse-glow {
            from { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }
            to { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
        }
        
        .feature-icon {
            transition: all 0.3s ease;
        }
        
        .feature-card:hover .feature-icon {
            transform: scale(1.2) rotate(10deg);
        }
        
        .bento-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }
        
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: rgba(59, 130, 246, 0.3) transparent;
        }
        
        .chat-container::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat-container::-webkit-scrollbar-track {
            background: rgba(59, 130, 246, 0.1);
            border-radius: 3px;
        }
        
        .chat-container::-webkit-scrollbar-thumb {
            background: rgba(59, 130, 246, 0.4);
            border-radius: 3px;
        }
        
        .chat-container::-webkit-scrollbar-thumb:hover {
            background: rgba(59, 130, 246, 0.6);
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            padding: 15px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }
        
        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #3b82f6;
            animation: typing 1.4s infinite ease-in-out;
            margin: 0 2px;
        }
        
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        

        
        .active-tab {
            background: rgba(59, 130, 246, 0.3) !important;
            border: 1px solid rgba(59, 130, 246, 0.6) !important;
            box-shadow: 0 0 30px rgba(59, 130, 246, 0.4), 
                       inset 0 0 20px rgba(59, 130, 246, 0.1) !important;
            transform: scale(1.05);
        }
        
        .loading-spinner {
            width: 20px;
            height: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            border-top: 2px solid #3b82f6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .floating-rocket { font-size: 4rem; }
            .gradient-text { font-size: 3rem; }
            .glass-card { margin: 0 1rem; padding: 1.5rem; }
            .bento-grid { grid-template-columns: 1fr; }
        }
        
        /* Better formatting for AI responses */
        .ai-response {
            line-height: 1.6;
        }
        
        .ai-response h1, .ai-response h2, .ai-response h3 {
            font-weight: bold;
            margin: 1rem 0 0.5rem 0;
            color: #60a5fa;
        }
        
        .ai-response p {
            margin-bottom: 1rem;
        }
        
        .ai-response ul, .ai-response ol {
            margin: 1rem 0;
            padding-left: 1.5rem;
        }
        
        .ai-response li {
            margin-bottom: 0.5rem;
        }
        
        .ai-response strong {
            color: #93c5fd;
            font-weight: 600;
        }
        
        /* Smooth scrolling for the entire page */
        html {
            scroll-behavior: smooth;
        }
        
        /* Navigation button hover effects */
        .nav-button {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.3));
            border: 1px solid rgba(59, 130, 246, 0.4);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .nav-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .nav-button:hover::before {
            left: 100%;
        }
        
        .nav-button:hover {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.35), rgba(37, 99, 235, 0.45));
            border: 1px solid rgba(59, 130, 246, 0.6);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
            transform: translateY(-1px);
        }
        
        /* Fade in animation for sections */
                .fade-in {
            opacity: 0;
            /* The transform property was the root cause of the bug and has been removed. */
            transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .fade-in.visible {
            opacity: 1;
        }
        
        /* Pulse animation for scroll indicators */
        @keyframes pulse-glow {
            0%, 100% { 
                box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 0 20px rgba(59, 130, 246, 0.8);
                transform: scale(1.05);
            }
        }
        
        .scroll-indicator {
            animation: pulse-glow 2s infinite;
        }
        
        /* Enhanced tab animations */
        .tab-content {
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .tab-content.hidden {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        
        .tab-content:not(.hidden) {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        
        .navbar-rocket-float {
            animation: navbar-float 6s ease-in-out infinite;
            display: inline-block;
        }

        @keyframes navbar-float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }

        /* Custom Scrollbar for all three results boxes */
#resume-results,
#interview-questions,
#skill-results {
    scrollbar-width: thin;
    scrollbar-color: rgba(59, 130, 246, 0.4) transparent;
}

#resume-results::-webkit-scrollbar,
#interview-questions::-webkit-scrollbar,
#skill-results::-webkit-scrollbar {
    width: 6px;
}

#resume-results::-webkit-scrollbar-track,
#interview-questions::-webkit-scrollbar-track,
#skill-results::-webkit-scrollbar-track {
    background: rgba(59, 130, 246, 0.1);
}

#resume-results::-webkit-scrollbar-thumb,
#interview-questions::-webkit-scrollbar-thumb,
#skill-results::-webkit-scrollbar-thumb {
    background: rgba(59, 130, 246, 0.4);
    border-radius: 3px;
}

#resume-results::-webkit-scrollbar-thumb:hover,
#interview-questions::-webkit-scrollbar-thumb:hover,
#skill-results::-webkit-scrollbar-thumb:hover {
    background: rgba(59, 130, 246, 0.6);
}
        
    </style>
</head>
<body class="bg-gradient-to-br from-blue-950 via-slate-900 to-blue-900 min-h-screen">


    <!-- Fixed Centered Pill-Shaped Navbar -->
<nav class="fixed top-6 left-1/2 transform -translate-x-1/2 z-50" id="navbar">

    <div class="transform scale-100 rounded-full overflow-hidden shadow-lg border border-blue-400/40">

<div class="backdrop-blur-xl bg-blue-950/60 transition-all duration-300">

            <div class="px-6 py-3 flex items-center justify-between space-x-8">
                
                <div class="flex items-center space-x-3">
                    <span class="text-2xl navbar-rocket-float">🚀</span>
                    <span class="gradient-text font-semibold text-lg hidden sm:block">AI Career Navigator</span>
                    <span class="gradient-text font-semibold text-base italic sm:hidden">Career AI</span>
                </div>
                
                <div class="hidden md:flex items-center space-x-1">
                    <a href="#home" onclick="smoothScrollToTop()" class="text-blue-100 hover:text-white px-4 py-2 rounded-full transition-all duration-300 hover:bg-blue-600/30 text-sm font-medium hover:scale-105">
                        Home
                    </a>
                    <a href="#features" onclick="smoothScrollTo('features')" class="text-blue-100 hover:text-white px-4 py-2 rounded-full transition-all duration-300 hover:bg-blue-600/30 text-sm font-medium hover:scale-105">
                        Features
                    </a>
                    <a href="#about" onclick="smoothScrollTo('about')" class="text-blue-100 hover:text-white px-4 py-2 rounded-full transition-all duration-300 hover:bg-blue-600/30 text-sm font-medium hover:scale-105">
                        About
                    </a>
                    <a href="#contact" onclick="smoothScrollTo('contact')" class="text-blue-100 hover:text-white px-4 py-2 rounded-full transition-all duration-300 hover:bg-blue-600/30 text-sm font-medium hover:scale-105">
                        Contact
                    </a>
                </div>
                
                <button id="mobile-menu-btn" class="md:hidden text-white p-2 rounded-full hover:bg-blue-600/40 transition-all duration-300">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>

            </div>
        </div>
    </div>

    <div id="mobile-menu" class="md:hidden hidden absolute top-full left-1/2 transform -translate-x-1/2 mt-2 z-40">
        <div class="px-6 py-4 rounded-xl backdrop-blur-xl bg-blue-950/60 border border-blue-400/40 shadow-2xl min-w-[200px]">
            <div class="space-y-2">
                <a href="#home" onclick="smoothScrollToTop(); toggleMobileMenu()" class="block text-blue-100 hover:text-white px-4 py-3 rounded-lg transition-all duration-300 hover:bg-blue-600/40 text-sm font-medium text-center">
                    Home
                </a>
                <a href="#features" onclick="smoothScrollTo('features'); toggleMobileMenu()" class="block text-blue-100 hover:text-white px-4 py-3 rounded-lg transition-all duration-300 hover:bg-blue-600/40 text-sm font-medium text-center">
                    Features
                </a>
                <a href="#about" onclick="smoothScrollTo('about'); toggleMobileMenu()" class="block text-blue-100 hover:text-white px-4 py-3 rounded-lg transition-all duration-300 hover:bg-blue-600/40 text-sm font-medium text-center">
                    About
                </a>
                <a href="#contact" onclick="smoothScrollTo('contact'); toggleMobileMenu()" class="block text-blue-100 hover:text-white px-4 py-3 rounded-lg transition-all duration-300 hover:bg-blue-600/40 text-sm font-medium text-center">
                    Contact
                </a>
            </div>
        </div>
    </div>
</nav>

    <!-- Main Content -->
    <main class="container mx-auto px-6 pt-24 pb-12">
        <!-- Hero Section -->
        <section class="text-center mb-16 fade-in">
            <div class="floating-rocket text-8xl mb-8">🚀</div>
            <h2 class="text-2xl font-semibold mb-2">
                <span class="text-blue-300 text-3xl" style="transform: scale(1.5); display: inline-block;">Your Personal</span>
            </h2>
            <h1 class="text-6xl font-black mb-6">
                <span class="gradient-text">AI Career Coach</span>
            </h1>
            <p class="text-xl text-gray-300 mb-12 max-w-4xl mx-auto leading-relaxed">
                A cutting-edge career guidance platform built with passion and precision. 
                Empowering professionals and students to make informed career decisions with AI-powered insights.
                Navigate your tech career journey with intelligent recommendations, resume optimization, 
                interview preparation, and skill development guidance.
            </p>
        </section>

        <!-- Feature Navigation Tabs -->
        <section id="features" class="mb-12 fade-in">
            <div class="flex flex-wrap justify-center gap-4 mb-8">
                 <button onclick="showTab('career-chat')" id="tab-career-chat" class="tab-button px-6 py-3 bg-blue-600/20 hover:bg-blue-600/30 text-white font-semibold active-tab rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 shadow-lg hover:shadow-blue-500/20">
                    💬 Career Chat
                </button>
                <button onclick="showTab('resume-analysis')" id="tab-resume-analysis" class="tab-button px-6 py-3 bg-blue-600/20 hover:bg-blue-600/30 text-white font-semibold rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 shadow-lg hover:shadow-blue-500/20">
                    📄 Resume Analysis
                </button>
                <button onclick="showTab('interview-prep')" id="tab-interview-prep" class="tab-button px-6 py-3 bg-blue-600/20 hover:bg-blue-600/30 text-white font-semibold rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 shadow-lg hover:shadow-blue-500/20">
                    🎯 Interview Prep
                </button>
                <button onclick="showTab('skill-analysis')" id="tab-skill-analysis" class="tab-button px-6 py-3 bg-blue-600/20 hover:bg-blue-600/30 text-white font-semibold rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 shadow-lg hover:shadow-blue-500/20">
                    🧠 Skill Analysis
            </div>
        </section>

        <!-- Tab Contents -->
        <section class="max-w-6xl mx-auto fade-in">
            <!-- Career Chat Tab -->
            <div id="career-chat" class="tab-content">
                <div class="glass-card p-8">
                    <div class="grid md:grid-cols-3 gap-8">
                        <!-- Profile Setup -->
                        <div class="space-y-6">
                            <h3 class="text-xl font-semibold text-white mb-4">Your Profile</h3>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Your Role:</label>
                                <input type="text" id="user-role" placeholder="e.g., Full Stack Developer" 
                                       class="w-full px-4 py-3 glass-card text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500">
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Experience:</label>
                                <div class="relative">
                                    <select id="user-experience" class="w-full px-4 py-3 glass-card text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl appearance-none bg-gray-800/50 border border-gray-600/30 focus:text-white" onchange="updateSelectColor(this)">
                                        <option value="" disabled selected class="text-gray-500">Click to select experience level</option>
                                        <option value="Entry Level (0-2 years)" class="text-white">Entry Level (0-2 years)</option>
                                        <option value="Mid Level (3-5 years)" class="text-white">Mid Level (3-5 years)</option>
                                        <option value="Senior Level (6+ years)" class="text-white">Senior Level (6+ years)</option>
                                        <option value="Lead/Manager (8+ years)" class="text-white">Lead/Manager (8+ years)</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Focus Area:</label>
                                <div class="relative">
                                    <select id="focus-area" class="w-full px-4 py-3 glass-card text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl appearance-none bg-gray-800/50 border border-gray-600/30 focus:text-white" onchange="updateSelectColor(this)">
                                        <option value="" disabled selected class="text-gray-500">Click to select focus area</option>
                                        <option value="Job Applications" class="text-white">Job Applications</option>
                                        <option value="Skill Development" class="text-white">Skill Development</option>
                                        <option value="Career Growth" class="text-white">Career Growth</option>
                                        <option value="Interview Preparation" class="text-white">Interview Preparation</option>
                                        <option value="Salary Negotiation" class="text-white">Salary Negotiation</option>
                                        <option value="Remote Work" class="text-white">Remote Work</option>
                                        <option value="Networking" class="text-white">Networking</option>
                                        <option value="Portfolio Building" class="text-white">Portfolio Building</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Chat Interface -->
                        <div class="md:col-span-2 space-y-6">
                            <div class="chat-container space-y-4 p-6 glass-card min-h-[400px]" id="chat-messages">
                                <div class="flex items-start space-x-3">
                                    <div class="text-2xl">🤖</div>
                                    <div class="glass-card p-4 max-w-lg">
                                        <p class="text-white"><strong>AI Career Mentor:</strong> Hello! I'm your AI Career Navigator specialized in tech careers. I can help you with internships, job applications, and career guidance. What would you like to discuss?</p>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="typing-indicator hidden items-center space-x-2 p-4" id="typing-indicator">
                                <div class="text-xl">🤖</div>
                                <div class="flex space-x-1">
                                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                                    <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                                </div>
                                <span class="text-gray-400 text-sm">AI is thinking...</span>
                            </div>
                            
                            <div class="flex space-x-3">
                                <input type="text" id="user-message" placeholder="Ask about tech careers, job applications, interviews..." 
                                       class="flex-1 px-4 py-3 glass-card text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                       onkeypress="if(event.key==='Enter') sendMessage()">
                                <button onclick="clearChat()" class="px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-red-500/25">
                                    🗑️ Clear
                                </button>
                                <button onclick="sendMessage()" class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-blue-500/25">
                                    💬 Send
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Resume Analysis Tab -->
            <div id="resume-analysis" class="tab-content hidden">
                <div class="glass-card p-8">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-2xl font-bold text-white">Resume Analysis</h3>
                        <button onclick="clearResumeAnalysis()" class="px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-red-500/25">
                            🗑️ Clear
                        </button>
                    </div>
                    <div class="grid md:grid-cols-2 gap-8">
                        <div class="space-y-6">
                            <!-- File Upload with Drag & Drop -->
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-3">Upload Resume (PDF/DOC/TXT):</label>
                                <div id="drop-zone" class="border-2 border-dashed border-gray-600 rounded-xl p-6 text-center bg-slate-800/30 hover:bg-slate-700/30 transition-colors cursor-pointer"
                                     ondrop="handleDrop(event)" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)"
                                     onclick="document.getElementById('resume-file').click()">
                                    <input type="file" id="resume-file" accept=".pdf,.doc,.docx,.txt" class="hidden" onchange="handleFileUpload(event)">
                                    <div class="flex flex-col items-center space-y-2">
                                        <div class="text-4xl mb-2">📄</div>
                                        <button type="button" class="px-6 py-3 bg-blue-600/20 hover:bg-blue-600/30 text-blue-200 rounded-lg transition-colors">
                                            Choose File
                                        </button>
                                        <p class="text-gray-400 text-sm">Or drag and drop your resume here</p>
                                        <p class="text-gray-500 text-xs">Supports: PDF, DOC, DOCX, TXT</p>
                                    </div>
                                    <p id="file-name" class="text-blue-300 text-sm mt-2"></p>
                                </div>
                            </div>
                            
                            <!-- Text Input Alternative -->
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-3">Or Paste Resume Text:</label>
                                <textarea id="resume-text" rows="8" placeholder="Paste your resume content here..." 
                                          class="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/30 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl"></textarea>
                            </div>
                            
                            <button onclick="analyzeResume()" class="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-emerald-500/25">
                                📊 Analyze Resume
                            </button>
                        </div>
                       <div class="bg-slate-800/50 border border-slate-600/30 rounded-xl p-6">
    
    <div id="resume-results" class="h-[640px] overflow-y-auto">
        <p class="text-gray-400">Upload your resume or paste text to get ATS optimization suggestions, keyword analysis, and formatting tips for tech roles.</p>
    </div>

</div>
                    </div>
                </div>
            </div>

            <!-- Interview Prep Tab -->
            <div id="interview-prep" class="tab-content hidden">
                <div class="glass-card p-8">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-2xl font-bold text-white">🎯 Interview Preparation</h3>
                        <button onclick="clearInterviewPrep()" class="px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-red-500/25">
                            🗑️ Clear
                        </button>
                    </div>
                    <div class="grid md:grid-cols-2 gap-8">
                        <div class="space-y-6">
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Role Type:</label>
                                <select id="interview-role" class="w-full px-4 py-3 glass-card text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl bg-gray-800/50 border border-gray-600/30" onchange="updateSelectColor(this)">
                                    <option value="" disabled selected class="text-gray-500">Click to select role type</option>
                                    <option value="Frontend Developer" class="text-white">Frontend Developer</option>
                                    <option value="Backend Developer" class="text-white">Backend Developer</option>
                                    <option value="Full Stack Developer" class="text-white">Full Stack Developer</option>
                                    <option value="MERN Stack Developer" class="text-white">MERN Stack Developer</option>
                                    <option value="DevOps Engineer" class="text-white">DevOps Engineer</option>
                                    <option value="Data Scientist" class="text-white">Data Scientist</option>
                                </select>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Target Company:</label>
                                <select id="target-company" class="w-full px-4 py-3 glass-card text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl bg-gray-800/50 border border-gray-600/30" onchange="updateSelectColor(this)">
                                    <option value="" disabled selected class="text-gray-500">Click to select target company</option>
                                    <option value="Google" class="text-white">Google</option>
                                    <option value="Microsoft" class="text-white">Microsoft</option>
                                    <option value="Amazon" class="text-white">Amazon</option>
                                    <option value="Meta" class="text-white">Meta</option>
                                    <option value="Apple" class="text-white">Apple</option>
                                    <option value="Netflix" class="text-white">Netflix</option>
                                    <option value="Startup" class="text-white">Startup</option>
                                    <option value="Mid-size Company" class="text-white">Mid-size Company</option>
                                    <option value="Enterprise" class="text-white">Enterprise</option>
                                </select>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Company Size:</label>
                                <select id="company-size" class="w-full px-4 py-3 glass-card text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl bg-gray-800/50 border border-gray-600/30" onchange="updateSelectColor(this)">
                                    <option value="" disabled selected class="text-gray-500">Click to select company size</option>
                                    <option value="Startup (1-50)" class="text-white">Startup (1-50)</option>
                                    <option value="Mid-size (51-500)" class="text-white">Mid-size (51-500)</option>
                                    <option value="Large (500+)" class="text-white">Large (500+)</option>
                                    <option value="Enterprise (1000+)" class="text-white">Enterprise (1000+)</option>
                                </select>
                            </div>
                            
                            <button onclick="generateQuestions()" class="w-full px-6 py-3 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-orange-500/25">
                                🎯 Generate Interview Questions
                            </button>
                        </div>
                        
                        <div class="glass-card p-6">

    <div id="interview-questions" class="h-[420px] overflow-y-auto">
        <p class="text-gray-400">Select your role and company type to get customized interview questions with the STAR method guidance.</p>
    </div>

</div>
                    </div>
                </div>
            </div>

            <!-- Skill Analysis Tab -->
<div id="skill-analysis" class="tab-content hidden">
    <div class="glass-card p-8">
        <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-white">🧠 Skill Gap Analysis</h3>
            <button onclick="clearSkillAnalysis()" class="px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-red-500/25">
                🗑️ Clear
            </button>
        </div>
        <div class="grid md:grid-cols-2 gap-8">
            <div class="space-y-6">
                <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">Target Role:</label>
                    <input type="text" id="target-role" placeholder="e.g., Senior MERN Stack Developer" class="w-full px-4 py-3 glass-card text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">Current Skills (comma-separated):</label>
                    <textarea id="current-skills" rows="4" placeholder="React, Node.js, MongoDB, Express.js, JavaScript, HTML, CSS..." class="w-full px-4 py-3 glass-card text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                </div>
                <button onclick="analyzeSkills()" class="w-full px-6 py-3 bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-700 hover:to-rose-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-pink-500/25">
                    🧠 Analyze Skills Gap
                </button>
            </div>
            
            <div class="glass-card p-6">
                <div id="skill-results" class="h-[520px] overflow-y-auto">
                    <p class="text-gray-400">Enter your target role and current skills to get a personalized learning roadmap with recommended resources.</p>
                </div>
            </div>

        </div>
    </div>
</div>
        </section>

        <!-- About Section -->
        <section id="about" class="mt-20 glass-card bg-blue-600/15 backdrop-blur-md border border-blue-500/20 mx-6 rounded-3xl p-8 md:p-12 shadow-2xl fade-in">
            <div class="text-center mb-16">
                <h2 class="text-5xl font-black text-white mb-6">About This Platform</h2>
                <div class="w-24 h-1 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-8"></div>
                <p class="text-xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
                    AI Career Navigator is an enterprise-grade career guidance platform engineered with cutting-edge AI technology. 
                    Designed to empower professionals and students with intelligent, data-driven career insights and strategic planning tools.
                </p>
            </div>
            
            <!-- Platform Overview -->
            <div class="grid lg:grid-cols-3 gap-8 mb-16">
                <div class="glass-card bg-blue-600/20 p-6 hover:bg-blue-500/25 transition-all duration-300 rounded-xl border border-blue-500/30">
                    <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold text-white mb-3">AI-Powered Intelligence</h3>
                    <p class="text-gray-300 text-sm leading-relaxed">
                        Leveraging Azure OpenAI's GPT-4.1 model for contextual understanding, 
                        natural language processing, and intelligent career recommendations based on industry trends and personal profiles.
                    </p>
                </div>
                
                <div class="glass-card bg-blue-600/20 p-6 hover:bg-blue-500/25 transition-all duration-300 rounded-xl border border-blue-500/30">
                    <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold text-white mb-3">Enterprise Architecture</h3>
                    <p class="text-gray-300 text-sm leading-relaxed">
                        Built on Microsoft Azure cloud infrastructure with robust security, scalability, and reliability. 
                        Implements modern software engineering practices and enterprise-grade development standards.
                    </p>
                </div>
                
                <div class="glass-card bg-blue-600/20 p-6 hover:bg-blue-500/25 transition-all duration-300 rounded-xl border border-blue-500/30">
                    <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold text-white mb-3">Professional Focus</h3>
                    <p class="text-gray-300 text-sm leading-relaxed">
                        Designed for career professionals, students, and organizations seeking strategic career development solutions. 
                        Addresses real-world challenges in talent management and professional growth planning.
                    </p>
                </div>
            </div>
            
            <!-- Technical Implementation -->
            <div class="grid md:grid-cols-2 gap-12">
                <div class="space-y-8">
                    <div class="glass-card bg-blue-600/20 p-6 rounded-xl border border-blue-500/30">
                        <h4 class="text-2xl font-semibold text-white mb-6 flex items-center">
                            <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                            </svg>
                            Technical Implementation
                        </h4>
                        <div class="space-y-4">
                            <div class="border-l-4 border-blue-500 pl-4">
                                <p class="text-gray-300 leading-relaxed">
                                    <strong class="text-blue-400">Azure OpenAI Integration:</strong> Direct API integration with GPT-4.1 deployment, 
                                    implementing advanced prompt engineering and context management for specialized career guidance conversations.
                                </p>
                            </div>
                            
                            <div class="border-l-4 border-blue-500 pl-4">
                                <p class="text-gray-300 leading-relaxed">
                                    <strong class="text-blue-400">Modern Web Architecture:</strong> RESTful API design with Flask backend, 
                                    responsive frontend using Tailwind CSS, and optimized for performance across all device categories.
                                </p>
                            </div>
                            
                            <div class="border-l-4 border-blue-500 pl-4">
                                <p class="text-gray-300 leading-relaxed">
                                    <strong class="text-blue-400">Security & Scalability:</strong> Enterprise-grade security protocols, 
                                    environment-based configuration management, and cloud-native deployment strategies for production readiness.
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="glass-card bg-blue-600/20 p-6 rounded-xl border border-blue-500/30">
                        <h4 class="text-2xl font-semibold text-white mb-6 flex items-center">
                            <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                            </svg>
                            Innovation & Purpose
                        </h4>
                        <p class="text-gray-300 leading-relaxed mb-4">
                            This platform addresses the critical gap in accessible, intelligent career guidance by democratizing 
                            professional coaching through artificial intelligence. The solution emerged from recognizing the challenges 
                            faced by professionals navigating complex career transitions in today's dynamic job market.
                        </p>
                        <p class="text-gray-300 leading-relaxed">
                            Built with a vision to provide <strong class="text-blue-400">strategic career insights</strong>, 
                            <strong class="text-blue-400">personalized guidance</strong>, and <strong class="text-blue-400">actionable recommendations</strong> 
                            that traditionally required expensive one-on-one coaching sessions.
                        </p>
                    </div>
                </div>
                
                <div class="space-y-6">
                    <div class="glass-card bg-blue-600/20 p-6 rounded-xl border border-blue-500/30">
                        <h4 class="text-2xl font-semibold text-white mb-6 flex items-center">
                            <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 7.172V5L8 4z"></path>
                            </svg>
                            Technology Stack
                        </h4>
                        
                        <!-- Frontend Technologies -->
                        <div class="mb-6">
                            <h5 class="text-lg font-medium text-blue-300 mb-3 flex items-center">
                                <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                                Frontend Development
                            </h5>
                            <div class="grid grid-cols-2 gap-3">
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">HTML5 & CSS3</div>
                                    <div class="text-xs text-gray-400">Semantic markup</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">Tailwind CSS</div>
                                    <div class="text-xs text-gray-400">Utility-first framework</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">JavaScript ES6+</div>
                                    <div class="text-xs text-gray-400">Modern JS features</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">Responsive Design</div>
                                    <div class="text-xs text-gray-400">Mobile-first approach</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Backend Technologies -->
                        <div class="mb-6">
                            <h5 class="text-lg font-medium text-blue-300 mb-3 flex items-center">
                                <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                                Backend Infrastructure
                            </h5>
                            <div class="grid grid-cols-2 gap-3">
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">Python 3.10+</div>
                                    <div class="text-xs text-gray-400">Core language</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">Flask Framework</div>
                                    <div class="text-xs text-gray-400">Web application</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">RESTful APIs</div>
                                    <div class="text-xs text-gray-400">Service architecture</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">CORS Support</div>
                                    <div class="text-xs text-gray-400">Cross-origin requests</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Cloud & AI -->
                        <div class="mb-4">
                            <h5 class="text-lg font-medium text-blue-300 mb-3 flex items-center">
                                <span class="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                                Cloud & AI Services
                            </h5>
                            <div class="grid grid-cols-1 gap-3">
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">Azure OpenAI Service</div>
                                    <div class="text-xs text-gray-400">GPT-4.1 deployment with enterprise security</div>
                                </div>
                                <div class="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                                    <div class="text-sm font-medium text-blue-300">Microsoft Azure Cloud</div>
                                    <div class="text-xs text-gray-400">Scalable infrastructure & monitoring</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="glass-card bg-blue-600/20 p-6 rounded-xl border border-blue-500/30">
                        <h4 class="text-xl font-semibold text-white mb-4 flex items-center">
                            <svg class="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                            </svg>
                            Design Philosophy
                        </h4>
                        <ul class="space-y-3 text-gray-300">
                            <li class="flex items-start">
                                <span class="w-1.5 h-1.5 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                                <span class="text-sm">Modern glassmorphism aesthetics with professional UX/UI design patterns</span>
                            </li>
                            <li class="flex items-start">
                                <span class="w-1.5 h-1.5 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                                <span class="text-sm">Accessibility-first approach compliant with WCAG 2.1 guidelines</span>
                            </li>
                            <li class="flex items-start">
                                <span class="w-1.5 h-1.5 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                                <span class="text-sm">Performance-optimized for sub-second load times across all devices</span>
                            </li>
                            <li class="flex items-start">
                                <span class="w-1.5 h-1.5 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></span>
                                <span class="text-sm">Enterprise-grade security and data protection standards</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Contact Section -->
    <footer id="contact" class="mt-20 glass-card bg-blue-600/15 backdrop-blur-md mx-32 mb-32 rounded-3xl p-8 md:p-12 shadow-2xl fade-in border border-blue-500/20">
        <div class="max-w-4xl mx-auto">
            <!-- Contact Header -->
            <div class="text-center mb-12">
                <h3 class="text-4xl font-bold text-white mb-4">Get In Touch</h3>
                <div class="w-24 h-1 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-4"></div>
                <p class="text-xl text-gray-300 max-w-2xl mx-auto">
                    Ready to accelerate your tech career? Connect with me for collaborations and opportunities.
                </p>
            </div>
            
            <!-- Contact Links -->
            <div class="flex flex-wrap justify-center gap-6 mb-16">
                <a href="mailto:aryanjstar3@gmail.com" class="flex items-center space-x-3 px-6 py-3 bg-blue-600/25 hover:bg-blue-600/35 text-blue-200 rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 backdrop-blur-sm">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                        <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                    </svg>
                    <span>aryanjstar3@gmail.com</span>
                </a>
                <a href="https://github.com/Aryanjstar/ai-career-navigator" target="_blank" class="flex items-center space-x-3 px-6 py-3 bg-blue-600/25 hover:bg-blue-600/35 text-blue-200 rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 backdrop-blur-sm">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clipRule="evenodd"/>
                    </svg>
                    <span>GitHub</span>
                </a>
                <a href="https://www.linkedin.com/in/aryanjstar/" target="_blank" class="flex items-center space-x-3 px-6 py-3 bg-blue-600/25 hover:bg-blue-600/35 text-blue-200 rounded-xl transition-all duration-300 hover:scale-105 border border-blue-400/30 backdrop-blur-sm">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                    <span>LinkedIn</span>
                </a>
            </div>
            
            <!-- Tech Stack Grid -->
            <div class="grid md:grid-cols-4 gap-8 mb-12">
                <div class="text-center bg-blue-600/20 rounded-xl p-4 border border-blue-500/30">
                    <h4 class="text-lg font-semibold text-blue-300 mb-4">Frontend</h4>
                    <div class="space-y-2 text-sm text-gray-300">
                        <p>HTML5 & CSS3</p>
                        <p>Tailwind CSS</p>
                        <p>Modern JavaScript</p>
                        <p>Responsive Design</p>
                    </div>
                </div>
                <div class="text-center bg-blue-600/20 rounded-xl p-4 border border-blue-500/30">
                    <h4 class="text-lg font-semibold text-blue-300 mb-4">Backend</h4>
                    <div class="space-y-2 text-sm text-gray-300">
                        <p>Python & Flask</p>
                        <p>REST APIs</p>
                        <p>Azure OpenAI</p>
                        <p>GPT-4.1 Integration</p>
                    </div>
                </div>
                <div class="text-center bg-blue-600/20 rounded-xl p-4 border border-blue-500/30">
                    <h4 class="text-lg font-semibold text-blue-300 mb-4">Azure Services</h4>
                    <div class="space-y-2 text-sm text-gray-300">
                        <p>Azure OpenAI Service</p>
                        <p>Azure App Service</p>
                        <p>Azure Monitor</p>
                        <p>Azure DevOps</p>
                    </div>
                </div>
                <div class="text-center bg-blue-600/20 rounded-xl p-4 border border-blue-500/30">
                    <h4 class="text-lg font-semibold text-blue-300 mb-4">MERN Stack</h4>
                    <div class="space-y-2 text-sm text-gray-300">
                        <p>MongoDB</p>
                        <p>Express.js</p>
                        <p>React.js</p>
                        <p>Node.js</p>
                    </div>
                </div>
            </div>
            
            <!-- Footer Bottom -->
            <div class="border-t border-gray-700 pt-8 text-center">
                <p class="text-lg text-gray-300 mb-2">
                    Built with ❤️ by <strong class="text-white">Aryan Jaiswal</strong>
                </p>
                <p class="text-sm text-gray-400 mb-4">
                    AI Career Navigator
                </p>
                <div class="flex flex-wrap justify-center items-center gap-4 text-xs text-gray-500">
                    <span>© 2025 Aryan Jaiswal</span>
                    <span>•</span>
                    <span>Professional Development Platform</span>
                    <span>•</span>
                    <span>AI-Powered Career Guidance</span>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Enhanced smooth scrolling functions
        function smoothScrollTo(elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }

        function smoothScrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
        



        // Initialize default tab and animations
        document.addEventListener('DOMContentLoaded', function() {
            showTab('career-chat');
            initScrollAnimations();
            initNavbarScroll();
            initMobileMenu();

            
            // Add smooth transition to body
            document.body.style.transition = 'transform 0.3s ease';
            
            // Add scroll indicator to navigation buttons
            const navButtons = document.querySelectorAll('.nav-button');
            navButtons.forEach(button => {
                button.addEventListener('mouseenter', () => {
                    button.classList.add('scroll-indicator');
                });
                button.addEventListener('mouseleave', () => {
                    button.classList.remove('scroll-indicator');
                });
            });
            
            // Initialize navbar scroll effects
            window.addEventListener('scroll', function() {
                updateNavbarOnScroll();
            });
            
            // Show first section immediately
            setTimeout(() => {
                const firstFadeElement = document.querySelector('.fade-in');
                if (firstFadeElement) {
                    firstFadeElement.classList.add('visible');
                }
            }, 100);
            
            // Add staggered animation for multiple fade-in elements
            setTimeout(() => {
                const fadeElements = document.querySelectorAll('.fade-in');
                fadeElements.forEach((el, index) => {
                    setTimeout(() => {
                        el.classList.add('visible');
                    }, index * 200);
                });
            }, 300);
        });
        
        // Enhanced smooth scroll to section with offset
        function smoothScrollToSection(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                // Add a subtle pulse effect to the target section
                element.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 300);
                
                const headerOffset = 100; // Account for header height
                const elementPosition = element.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }

        // Navbar scroll effects
        function initNavbarScroll() {
            const navbar = document.getElementById('navbar');
            let lastScrollTop = 0;
            
            function updateNavbarOnScroll() {
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                
                if (scrollTop > 50) {
                    navbar.classList.add('bg-blue-950/95');
                    navbar.classList.remove('bg-blue-950/80');
                } else {
                    navbar.classList.add('bg-blue-950/80');
                    navbar.classList.remove('bg-blue-950/95');
                }
                
                lastScrollTop = scrollTop;
            }
            
            // Make updateNavbarOnScroll available globally
            window.updateNavbarOnScroll = updateNavbarOnScroll;
        }

        // Mobile menu functionality
        function initMobileMenu() {
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            const mobileMenu = document.getElementById('mobile-menu');
            
            if (mobileMenuBtn && mobileMenu) {
                mobileMenuBtn.addEventListener('click', toggleMobileMenu);
            }
        }

        function toggleMobileMenu() {
            const mobileMenu = document.getElementById('mobile-menu');
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            
            if (mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.remove('hidden');
                mobileMenuBtn.innerHTML = `
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                `;
            } else {
                mobileMenu.classList.add('hidden');
                mobileMenuBtn.innerHTML = `
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                `;
            }
        }

        // Smooth scroll functions
        function smoothScrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        function smoothScrollTo(sectionId) {
            smoothScrollToSection(sectionId);
        }
        
        // Intersection Observer for fade-in animations
        function initScrollAnimations() {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, observerOptions);

            // Observe all fade-in elements
            document.querySelectorAll('.fade-in').forEach(el => {
                observer.observe(el);
            });
        }
        
        // Tab Management
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.add('hidden');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active-tab');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.remove('hidden');
            document.getElementById(`tab-${tabName}`).classList.add('active-tab');
        }
        
        // Update select element text color when option is selected
        function updateSelectColor(selectElement) {
            if (selectElement.value && selectElement.value !== '') {
                // If a valid option is selected, make text white
                selectElement.style.color = '#ffffff';
            } else {
                // If no option or placeholder is selected, keep it gray
                selectElement.style.color = '#9ca3af';
            }
        }
        
        // Format AI response text with better HTML rendering
        function formatAIResponse(text) {
            if (!text) return '';
            
            // The response is already in HTML format from the API, so we just need to ensure it's safe
            // Remove any excessive asterisks that might have slipped through
            text = text.replace(/\*\*\*+/g, '');
            text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
            text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
            
            return text;
        }

        // Enhanced Chat Functionality with better error handling
        async function sendMessage() {
            const messageInput = document.getElementById('user-message');
            const message = messageInput.value.trim();
            
            if (!message) {
                alert('Please enter a message before sending.');
                return;
            }

            const userRole = document.getElementById('user-role').value;
            const experience = document.getElementById('user-experience').value;
            const focusArea = document.getElementById('focus-area').value;

            // Add user message to chat
            addMessage('user', message);
            messageInput.value = '';

            // Show typing indicator
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.classList.remove('hidden');
                typingIndicator.classList.add('flex');
            }

            try {
                console.log('Sending message:', { message, userRole, experience, focusArea });
                
                const response = await fetch('/api/career-chat', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        user_role: userRole,
                        experience: experience,
                        focus_area: focusArea
                    })
                });

                console.log('Response status:', response.status);
                
                const data = await response.json();
                console.log('Response data:', data);
                
                // Hide typing indicator
                if (typingIndicator) {
                    typingIndicator.classList.add('hidden');
                    typingIndicator.classList.remove('flex');
                }

                if (data.error) {
                    // Show helpful error message from backend
                    addMessage('ai', `<div class="bg-yellow-600/20 border border-yellow-500/30 rounded-lg p-3 mb-2">
                        <div class="flex items-center space-x-2">
                            <span class="text-yellow-400">⚠️</span>
                            <strong class="text-yellow-400">Profile Setup Required</strong>
                        </div>
                        <p class="text-gray-300 mt-2">${data.error}</p>
                        <p class="text-gray-400 text-sm mt-2">Please use the dropdown menus above to select your role, experience level, and focus area first.</p>
                    </div>`);
                } else if (data.response) {
                    addMessage('ai', data.response);
                } else {
                    addMessage('ai', 'Sorry, I received an empty response. Please try again.');
                }
            } catch (error) {
                console.error('Chat error:', error);
                
                // Hide typing indicator
                if (typingIndicator) {
                    typingIndicator.classList.add('hidden');
                    typingIndicator.classList.remove('flex');
                }
                
                addMessage('ai', `Connection error: ${error.message}. Please check your internet connection and try again.`);
            }
        }

        function addMessage(sender, message) {
            const chatContainer = document.getElementById('chat-messages');
            if (!chatContainer) {
                console.error('Chat container not found');
                return;
            }
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'mb-4'; // Add spacing between messages
            
            if (sender === 'user') {
                // Escape HTML in user message for security
                const escapedMessage = message.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                messageDiv.innerHTML = `
                    <div class="flex items-start space-x-3 justify-end">
                        <div class="glass-card p-4 max-w-lg bg-blue-600/20 rounded-xl">
                            <p class="text-white">${escapedMessage}</p>
                        </div>
                        <div class="text-2xl">👤</div>
                    </div>
                `;
            } else {
                // AI messages are already formatted HTML from the backend
                const formattedMessage = formatAIResponse(message);
                messageDiv.innerHTML = `
                    <div class="flex items-start space-x-3">
                        <div class="text-2xl">🤖</div>
                        <div class="glass-card p-4 max-w-3xl rounded-xl">
                            <div class="text-white ai-response">${formattedMessage}</div>
                        </div>
                    </div>
                `;
            }
            
            chatContainer.appendChild(messageDiv);
            
            // Smooth scroll to bottom
            // Conditionally scroll based on the message sender.
        setTimeout(() => {
            if (sender === 'ai') {
                // For AI responses, scroll to the TOP of the new message.
                // This is crucial for long answers, so the user can start reading from the beginning.
                chatContainer.scrollTo({ top: messageDiv.offsetTop, behavior: 'smooth' });
            } else {
                // For the user's own message, scroll to the BOTTOM of the chat container.
                // This keeps the chat input in view and shows the latest part of the conversation.
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }, 100);
        }

        // Enhanced Resume Analysis - Works with EITHER file upload OR text input
        async function analyzeResume() {
            const resumeText = document.getElementById('resume-text').value.trim();
            const fileInput = document.getElementById('resume-file');
            const uploadedFile = fileInput.files[0];
            
            // Check if we have either text OR file
            if (!resumeText && !uploadedFile) {
                alert('Please either paste your resume text OR upload a resume file.');
                return;
            }

            const resultsDiv = document.getElementById('resume-results');
            resultsDiv.innerHTML = '<div class="flex items-center justify-center space-x-2 p-4"><div class="animate-spin rounded-full h-6 w-6 border-b-2 border-green-400"></div><span class="text-gray-400">Analyzing your resume...</span></div>';

            try {
                console.log('Analyzing resume...');
                
                let requestBody;
                let headers;
                
                if (uploadedFile) {
                    // Handle file upload
                    const formData = new FormData();
                    formData.append('resume_file', uploadedFile);
                    if (resumeText) {
                        formData.append('resume_text', resumeText);
                    }
                    
                    requestBody = formData;
                    headers = { 'Accept': 'application/json' }; // Don't set Content-Type for FormData
                } else {
                    // Handle text input only
                    requestBody = JSON.stringify({ resume_text: resumeText });
                    headers = { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    };
                }
                
                const response = await fetch('/api/resume-analysis', {
                    method: 'POST',
                    headers: headers,
                    body: requestBody
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Resume analysis response:', data);
                
                if (data.error) {
                    resultsDiv.innerHTML = `<p class="text-red-400">Error: ${data.error}</p>`;
                } else if (data.analysis) {
                    const formattedAnalysis = formatAIResponse(data.analysis);
                    resultsDiv.innerHTML = `<div class="space-y-4"><h4 class="text-lg font-semibold text-white">📊 Analysis Results:</h4><div class="text-gray-300 ai-response">${formattedAnalysis}</div></div>`;
                } else {
                    resultsDiv.innerHTML = '<p class="text-red-400">No analysis received. Please try again.</p>';
                }
            } catch (error) {
                console.error('Resume analysis error:', error);
                resultsDiv.innerHTML = `<p class="text-red-400">Connection error: ${error.message}</p>`;
            }
        }

        // Enhanced Interview Questions Generation
        async function generateQuestions() {
            const role = document.getElementById('interview-role').value;
            const targetCompany = document.getElementById('target-company').value;
            const companySize = document.getElementById('company-size').value;

            const questionsDiv = document.getElementById('interview-questions');
            questionsDiv.innerHTML = '<div class="flex items-center justify-center space-x-2 p-4"><div class="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-400"></div><span class="text-gray-400">Generating interview questions...</span></div>';

            try {
                console.log('Generating interview questions for:', { role, targetCompany, companySize });
                
                const response = await fetch('/api/interview-prep', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ 
                        role: role, 
                        target_company: targetCompany, 
                        company_size: companySize 
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Interview prep response:', data);
                
                if (data.error) {
                    questionsDiv.innerHTML = `<p class="text-red-400">Error: ${data.error}</p>`;
                } else if (data.questions) {
                    const formattedQuestions = formatAIResponse(data.questions);
                    questionsDiv.innerHTML = `<div class="space-y-4"><h4 class="text-lg font-semibold text-white">Interview Preparation:</h4><div class="text-gray-300 ai-response">${formattedQuestions}</div></div>`;
                } else if (data.response) {
                    // Show friendly backend message (e.g. missing dropdowns)
                    questionsDiv.innerHTML = `<div class="text-gray-400 ai-response">${data.response}</div>`;
                } else {
                    questionsDiv.innerHTML = `<p class="text-red-400">No questions received. Please try again.</p>`;
                }
            } catch (error) {
                console.error('Interview prep error:', error);
                questionsDiv.innerHTML = `<p class="text-red-400">Connection error: ${error.message}</p>`;
            }
        }

        // Enhanced Skill Analysis
        async function analyzeSkills() {
            const targetRole = document.getElementById('target-role').value.trim();
            const currentSkills = document.getElementById('current-skills').value.trim();

            if (!targetRole || !currentSkills) {
                alert('Please fill in both target role and current skills.');
                return;
            }

            const resultsDiv = document.getElementById('skill-results');
            resultsDiv.innerHTML = '<div class="flex items-center justify-center space-x-2 p-4"><div class="animate-spin rounded-full h-6 w-6 border-b-2 border-orange-400"></div><span class="text-gray-400">Analyzing skill gaps...</span></div>';

            try {
                console.log('Analyzing skills for:', { targetRole, currentSkills });
                
                const response = await fetch('/api/skill-analysis', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ 
                        target_role: targetRole, 
                        current_skills: currentSkills 
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Skill analysis response:', data);
                
                if (data.error) {
                    resultsDiv.innerHTML = `<p class="text-red-400">Error: ${data.error}</p>`;
                } else if (data.analysis) {
                    const formattedAnalysis = formatAIResponse(data.analysis);
                    resultsDiv.innerHTML = `<div class="space-y-4"><h4 class="text-lg font-semibold text-white">🧠 Skill Gap Analysis:</h4><div class="text-gray-300 ai-response">${formattedAnalysis}</div></div>`;
                } else {
                    resultsDiv.innerHTML = '<p class="text-red-400">No analysis received. Please try again.</p>';
                }
            } catch (error) {
                console.error('Skill analysis error:', error);
                resultsDiv.innerHTML = `<p class="text-red-400">Connection error: ${error.message}</p>`;
            }
        }

        // File Upload Handler with text extraction
        function handleFileUpload(event) {
            const file = event.target.files[0];
            processFile(file);
        }

        // Drag and Drop Handlers
        function handleDragOver(event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
            const dropZone = document.getElementById('drop-zone');
            dropZone.classList.add('border-blue-500', 'bg-blue-600/10');
        }

        function handleDragLeave(event) {
            event.preventDefault();
            const dropZone = document.getElementById('drop-zone');
            dropZone.classList.remove('border-blue-500', 'bg-blue-600/10');
        }

        function handleDrop(event) {
            event.preventDefault();
            const dropZone = document.getElementById('drop-zone');
            dropZone.classList.remove('border-blue-500', 'bg-blue-600/10');
            
            const files = event.dataTransfer.files;
            if (files.length > 0) {
                processFile(files[0]);
            }
        }

        // Process uploaded file
        function processFile(file) {
            if (!file) return;
            
            document.getElementById('file-name').textContent = `Selected: ${file.name}`;
            
            // Read file content if it's a text-based file
            if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('resume-text').value = e.target.result;
                    alert('✅ TXT file content loaded! You can now analyze your resume.');
                };
                reader.readAsText(file);
            } else if (file.name.endsWith('.pdf') || file.name.endsWith('.doc') || file.name.endsWith('.docx')) {
                alert('📎 File uploaded! You can now click "Analyze Resume" to proceed, or copy and paste your resume text into the text area for better accuracy.');
            } else {
                alert('❌ Unsupported file format. Please upload a TXT file or copy and paste your resume text into the text area.');
            }
        }



        // Clean up function to remove any unwanted scroll progress elements
        function cleanupScrollProgress() {
            // Remove any elements with scroll-progress class or id
            const scrollProgressElements = document.querySelectorAll(
                '.scroll-progress, #scrollProgress, #scroll-progress, [class*="scroll"], [id*="scroll"], [class*="progress"], [id*="progress"]'
            );
            
            scrollProgressElements.forEach(element => {
                // Only remove if it's not part of our main UI
                if (!element.closest('#navbar') && 
                    !element.closest('.glass-card') && 
                    !element.closest('.loading-spinner') &&
                    !element.classList.contains('chat-container')) {
                    element.remove();
                    console.log('Removed scroll progress element:', element);
                }
            });
            
            // Remove any fixed positioned elements at top that might be blue rectangles
            const fixedElements = document.querySelectorAll('[style*="position: fixed"][style*="top: 0"]');
            fixedElements.forEach(element => {
                if (!element.closest('#navbar') && element.style.backgroundColor && element.style.backgroundColor.includes('blue')) {
                    element.remove();
                    console.log('Removed fixed blue element:', element);
                }
            });
        }

        // Run cleanup on page load
        document.addEventListener('DOMContentLoaded', function() {
            cleanupScrollProgress();
            
            // Run cleanup periodically to catch any dynamically added elements
            setInterval(cleanupScrollProgress, 1000);
        });

        // Also run cleanup when the page becomes visible (handles browser back/forward)
        document.addEventListener('visibilitychange', function() {
            if (!document.hidden) {
                cleanupScrollProgress();
            }
        });

        // Clear Chat Function
        function clearChat() {
            const chatMessages = document.getElementById('chat-messages');
            const userMessage = document.getElementById('user-message');
            
            // Reset chat to initial state
            chatMessages.innerHTML = `
                <div class="flex items-start space-x-3">
                    <div class="text-2xl">🤖</div>
                    <div class="glass-card p-4 max-w-lg">
                        <p class="text-white"><strong>AI Career Mentor:</strong> Hello! I'm your AI Career Navigator specialized in tech careers. I can help you with internships, job applications, and career guidance. What would you like to discuss?</p>
                    </div>
                </div>
            `;
            
            // Clear input field
            userMessage.value = '';
            
            // Hide typing indicator if visible
            const typingIndicator = document.getElementById('typing-indicator');
            if (typingIndicator) {
                typingIndicator.classList.add('hidden');
            }
        }

        // Clear Resume Analysis Function
        function clearResumeAnalysis() {
            // Clear file input
            const fileInput = document.getElementById('resume-file');
            fileInput.value = '';
            
            // Clear text area
            const resumeText = document.getElementById('resume-text');
            resumeText.value = '';
            
            // Clear file name display
            const fileName = document.getElementById('file-name');
            fileName.textContent = '';
            
            // Reset results
            const resultsDiv = document.getElementById('resume-results');
            resultsDiv.innerHTML = '<p class="text-gray-400">Upload your resume or paste text to get ATS optimization suggestions, keyword analysis, and formatting tips for tech roles.</p>';
        }

        // Clear Interview Prep Function
        function clearInterviewPrep() {
            // Reset dropdowns to default values
            const interviewRole = document.getElementById('interview-role');
            interviewRole.selectedIndex = 0;
            
            const targetCompany = document.getElementById('target-company');
            targetCompany.selectedIndex = 0;
            
            const companySize = document.getElementById('company-size');
            companySize.selectedIndex = 0;
            
            // Clear results
            const questionsDiv = document.getElementById('interview-questions');
            questionsDiv.innerHTML = '<p class="text-gray-400">Select your target role and company to get customized interview questions and preparation tips.</p>';
        }

        // Clear Skill Analysis Function
        function clearSkillAnalysis() {
            // Clear input fields
            const targetRole = document.getElementById('target-role');
            targetRole.value = '';
            
            const currentSkills = document.getElementById('current-skills');
            currentSkills.value = '';
            
            // Clear results
            const resultsDiv = document.getElementById('skill-results');
            resultsDiv.innerHTML = '<p class="text-gray-400">Enter your target role and current skills to get personalized skill gap analysis and learning recommendations.</p>';
        }

        // Set initial color for interview prep selects on page load
        window.addEventListener('DOMContentLoaded', function() {
            ['interview-role', 'target-company', 'company-size'].forEach(function(id) {
                var el = document.getElementById(id);
                if (el) updateSelectColor(el);
            });
        });




    </script>
</body>
</html>
"""

def extract_text_from_file(file):
    """Extract text from uploaded files (PDF, DOC, DOCX, TXT)"""
    try:
        filename = file.filename.lower()
        
        if filename.endswith('.txt'):
            return file.read().decode('utf-8')
            
        elif filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif filename.endswith(('.doc', '.docx')):
            doc = Document(io.BytesIO(file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
            
        else:
            raise ValueError("Unsupported file format")
            
    except Exception as e:
        logger.error(f"File extraction error: {e}")
        raise Exception(f"Failed to extract text from file: {e}")

def get_ai_response(prompt, max_tokens=1500):
    """Get response from Azure OpenAI"""
    if not client:
        return "Azure OpenAI client not configured properly."
    
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": """You are an expert AI Career Navigator specializing in tech careers.

                **Core Instructions:**
                - Your tone must always be friendly,professional, encouraging, and helpful.
                - Address the user directly as "you". Do not invent, use, or ask for the user's name.
                - Provide detailed, actionable, and specific advice tailored to the user's context.
                - When the user's prompt provides a specific structure or format, you MUST follow it precisely.
                - For any non-career-related questions, respond with: "I'm focused on career guidance only. Please ask about your tech career, job applications, interviews, or skill development."
                - Use HTML for formatting, such as `<h4>`, `<strong>`, `<ul>`, and `<li>` for clarity. Do not use markdown asterisks.
                """},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return f"I encountered an error processing your request. Please try again."

@app.route('/')
def home():
    """Render the beautiful AI Career Navigator homepage"""
    return render_template_string(CAREER_NAVIGATOR_TEMPLATE)

@app.route('/config')
def config():
    """API configuration endpoint"""
    return jsonify({
        "platform": "MERN Stack Career Navigator",
        "version": "2.0.0",
        "ai": {
            "model": AZURE_OPENAI_MODEL,
            "deployment": AZURE_OPENAI_DEPLOYMENT,
            "endpoint_configured": bool(AZURE_OPENAI_ENDPOINT),
            "api_key_configured": bool(AZURE_OPENAI_API_KEY)
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

@app.route('/api/career-chat', methods=['POST'])
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
        
        response = get_ai_response(prompt, max_tokens=1500)
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/resume-analysis', methods=['POST'])
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
        
        analysis = get_ai_response(prompt, max_tokens=2000)
        
        return jsonify({
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/interview-prep', methods=['POST'])
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
        **Act as an experienced Hiring Manager and Interview Coach at a leading tech company like '{target_company}'.** The user is preparing for an interview.

        **Candidate Profile:**
        - **Target Role:** {role}
        - **Target Company:** {target_company}
        - **Company Size/Type:** {company_size}

        **Your Task:**
        Generate a detailed and highly realistic interview preparation guide tailored specifically to this profile. Go beyond generic questions and provide deep insights.

        **Required Preparation Briefing:**

        1.  **Company & Role-Specific Intelligence:** Based on '{target_company}' and the '{role}', what are the likely core values and technical competencies they will be screening for? (e.g., For Google, it's scalability and data structures; for a startup, it's product sense and execution speed).

        2.  **Technical Questions (with "What We're Looking For" insight):**
            * Provide 2-3 deep, role-specific technical questions.
            * For each question, add a section titled "**What the Interviewer is Looking For:**" that explains the concepts being tested and what a great answer reveals about the candidate's thinking process (e.g., "We are testing your understanding of React's reconciliation algorithm and your ability to reason about performance trade-offs.").

        3.  **Behavioral Question (Deep Dive with the S.T.A.R. Method):**
            * Provide one challenging behavioral question relevant to the role (e.g., "Tell me about a time you had a major disagreement with a colleague on a technical decision.").
            * Provide a detailed guide on how to structure an answer using the **S.T.A.R. (Situation, Task, Action, Result)** method, including a sample answer outline. Explain *why* this structure is so effective for storytelling.

        4.  **Questions for *You* to Ask the Interviewer:**
            * Suggest 2-3 insightful questions the user should ask. These should not be about salary. They should demonstrate intelligence and genuine interest (e.g., "What is the biggest technical challenge the team is facing in the next six months?" or "How do you measure success for someone in this role?").

        5.  **Final Preparation Strategy:** Provide a final checklist for the 48 hours leading up to the interview.
        """
        
        response_text = get_ai_response(prompt, max_tokens=1500)
        
        return jsonify({
            "response": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Interview prep error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/skill-analysis', methods=['POST'])
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
        
        analysis = get_ai_response(prompt, max_tokens=1500)
        
        return jsonify({
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Skill analysis error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting AI Career Navigator Pro...")
    logger.info(f"Azure OpenAI Endpoint: {AZURE_OPENAI_ENDPOINT}")
    logger.info(f"Azure OpenAI Model: {AZURE_OPENAI_MODEL}")
    
    app.run(host='0.0.0.0', port=8000, debug=True) 