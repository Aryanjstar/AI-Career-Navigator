# 🎯 AI Career Navigator — <ins>v1</ins>

[![Azure](https://img.shields.io/badge/Azure-OpenAI-0078d4.svg)](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/)
[![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-3178c6.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-3776ab.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **🚀 AI-powered career development platform that transforms job searching into strategic career growth**  
> 📌 **Version: v1** — First public release with core features like resume analysis, job matching, and interview prep.

<p align="center">
  
</p>

### 🎬 Video Walkthrough
See the AI Career Navigator in action!

🔇 Due to browser restrictions, the video is muted by default. If you'd like to hear the audio, please unmute it.

https://github.com/user-attachments/assets/51b16261-615e-4104-a1bc-867575344d2b


An intelligent career guidance platform that analyzes resumes, identifies skill gaps, generates interview questions, and provides personalized career roadmaps using Azure OpenAI and modern web technologies.

---

## ✨ What This Does

- **📄 Smart Resume Analysis**: Upload your resume and get instant AI-powered insights  
- **🎯 Job Matching**: Compare your skills against job descriptions with precision scoring  
- **📚 Skill Gap Analysis**: Identify missing skills and get learning recommendations  
- **🤝 Interview Preparation**: Generate role-specific interview questions  
- **📊 Career Analytics**: Track your progress and get market insights  

---

## 🎭 My Story & Motivation

> *"Every developer deserves a career that matches their potential"*

As a developer who's navigated the challenging tech job market, I've experienced firsthand the frustration of:
- **Endless Applications**: Sending hundreds of resumes into the void  
- **Skill Confusion**: Not knowing which technologies to learn next  
- **Interview Anxiety**: Walking into interviews unprepared  
- **Salary Uncertainty**: Not knowing my market value  

I built AI Career Navigator because I believe **technology should empower careers, not just companies**. This platform is my answer to the question:  
*"What if every developer had a personal career advisor powered by AI?"*

### 💡 The Vision
I wanted to create something that would have helped me earlier in my career - a tool that:
- Gives honest, actionable feedback on resumes  
- Shows exactly which skills matter for specific roles  
- Prepares you for interviews with real, relevant questions  
- Tracks your growth and celebrates your progress  

This isn't just another job board or generic career advice site. It's a **personalized AI career coach** that understands the modern tech landscape and helps developers like us make strategic career decisions.

---

## 🚀 Quick Start

### 📋 Prerequisites
- Node.js 20+ and npm  
- Python 3.11+ and pip  
- Azure subscription  
- Git  

### ⚡ One-Click Deployment
```bash
# Clone and deploy to Azure
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Authenticate with Azure
azd auth login

# Deploy everything to Azure
azd up
````

### 🛠️ Local Development

```bash
# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Set up environment variables (see docs/SETUP.md)
cp .env.example .env

# Run backend
cd backend && python -m uvicorn app:app --reload --port 8000

# Run frontend (new terminal)
cd frontend && npm run dev
```

**Local URLs:**

* Frontend: [http://localhost:5173](http://localhost:5173)
* Backend API: [http://localhost:8000](http://localhost:8000)
* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🏗️ Architecture

**Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
**Backend**: FastAPI + Python + Azure OpenAI
**Database**: SQLite (dev) / PostgreSQL (prod)
**Deployment**: Azure Container Apps + Azure OpenAI Service

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │───▶│   FastAPI        │───▶│  Azure OpenAI   │
│   (Frontend)    │    │   (Backend)      │    │   (GPT-4)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  File Upload    │    │  Resume Parser   │    │  AI Analysis    │
│  & Validation   │    │  & Processor     │    │  & Insights     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 📚 Documentation

* **[📖 Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
* **[🏗️ Architecture](docs/ARCHITECTURE.md)** - Technical deep dive and system design
* **[🔧 Development](docs/DEVELOPMENT.md)** - Contributing and development workflow
* **[🚀 Deployment](docs/DEPLOYMENT.md)** - Production deployment guide
* **[💰 Cost Analysis](docs/COST_ANALYSIS.md)** - Azure resource costs and optimization
* **[🔒 Security](docs/SECURITY.md)** - Security implementation and best practices
* **[🛣️ Roadmap](docs/ROADMAP.md)** - Future features and development plans
* **[❓ FAQ](docs/FAQ.md)** - Common questions and troubleshooting

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with modern technologies and Azure AI services. Special thanks to the open-source community and Microsoft Azure for making this possible.

---

## 🔗 Links

* **Live Demo**: [ai-career-navigator.azurewebsites.net](https://ai-career-navigator.azurewebsites.net)
* **Documentation**: [docs/](docs/)
* **Issues**: [GitHub Issues](https://github.com/Aryanjstar/AI-Career-Navigator/issues)
* **Discussions**: [GitHub Discussions](https://github.com/Aryanjstar/AI-Career-Navigator/discussions)

---

<div align="center">

**🚀 Built with ❤️ for developers seeking better careers**

⭐ Star this repo if it helped you | 🐛 Report bugs | 💡 Suggest features

</div>
```
