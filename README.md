 🎯 AI Career Navigator

[![Azure](https://img.shields.io/badge/Azure-OpenAI-blue.svg)](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Transform your career with AI-powered resume analysis, skill gap identification, and personalized interview preparation.**

A modern, full-stack web application that revolutionizes career development through advanced AI technologies. Built with Azure OpenAI, React, and cutting-edge 3D visualizations.

### 🎬 Video Walkthrough  
See AI Career Navigator in action!

🔇 *Note: The GitHub-hosted video below may be muted by default due to browser restrictions. Please unmute to hear the audio.*

📽️ Demo Video:  

https://github.com/user-attachments/assets/d84e24d1-8106-4456-a8fe-b8b9fdac8552

<p align="center">
  ▶️ Prefer YouTube? <a href="https://youtu.be/t_e-CtLxn_Q">Watch it here</a>
</p>

## 🌟 Features

### 🎯 Phase 1: Core MVP

- ✅ **Smart Resume Analysis**: AI-powered resume parsing and job description matching
- ✅ **Match Score Calculation**: Precision scoring (0-100%) based on skills and requirements
- ✅ **Skill Gap Identification**: Detailed analysis of missing skills and competencies
- ✅ **Modern 3D Interface**: Interactive Three.js visualizations and animations
- ✅ **Responsive Design**: Tailwind CSS with mobile-first approach

### 📊 Phase 2: Advanced Features

- ✅ **Interview Question Generation**: Role-specific technical and behavioral questions
- ✅ **Resume Enhancement**: AI-powered suggestions for optimization
- ✅ **Salary Insights**: Market-based compensation analysis
- ✅ **Interactive Dashboard**: Real-time analytics and progress tracking
- ✅ **File Upload Support**: PDF, DOC, DOCX, and TXT resume formats

### 🚀 Phase 3: Community & Analytics

- ✅ **Career Analytics**: Industry trends and skill demand insights
- ✅ **Learning Recommendations**: Personalized skill development paths
- ✅ **Progress Tracking**: Career development timeline and milestones
- ✅ **Community Insights**: Anonymized skill gap trends
- ✅ **Export Capabilities**: PDF reports and portfolio generation

## 🏗️ Architecture

![Architecture Diagram](docs/images/architecture.png)

### Technology Stack

**Frontend:**

- **React 18.3** with TypeScript for type-safe development
- **Three.js & React Three Fiber** for 3D visualizations and animations
- **Framer Motion** for smooth animations and interactions
- **Tailwind CSS** for modern, responsive styling
- **Recharts** for data visualization and analytics
- **React Dropzone** for drag-and-drop file uploads

**Backend:**

- **Python 3.11** with Flask for lightweight, production-ready APIs
- **Azure OpenAI Service** with GPT-3.5-Turbo/GPT-4 for intelligent analysis
- **Gunicorn** with gthread workers for production deployment
- **Response Caching** for cost optimization and faster responses
- **Rate Limiting** for API protection and fair usage

**Infrastructure:**

- **Azure App Service** for scalable web hosting
- **Azure Container Registry** for containerized deployments
- **Azure Application Insights** for monitoring and analytics
- **Azure Key Vault** for secure credential management

## 🚀 Quick Start

### Prerequisites

- **Node.js 20+** and npm
- **Python 3.11+** and pip
- **Azure Subscription** with OpenAI service
- **Git** for version control

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Install dependencies
npm install
cd app/backend && pip install -r requirements.txt
```

### 2. Configure Azure Services

```bash
# Set up Azure Developer CLI
azd auth login
azd env new ai-career-navigator

# Configure OpenAI credentials (replace with your values)
azd env set OPENAI_API_KEY "your-openai-api-key"
azd env set OPENAI_ENDPOINT "https://your-resource.openai.azure.com/"
azd env set AZURE_OPENAI_CHATGPT_MODEL "gpt-4"
```

### 3. Deploy to Azure

```bash
# Deploy everything with one command
azd up

# Or run locally for development
cd app/frontend && npm run dev  # Frontend on http://localhost:5173
cd app/backend && python -m flask run --host 0.0.0.0 --port 8000  # Backend on http://localhost:8000
```

### 🌐 Live Demo

**[https://ai-career-navigator-backend.azurewebsites.net](https://ai-career-navigator-backend.azurewebsites.net)**

## 📸 Screenshots

<details>
<summary>🎨 Modern UI Gallery</summary>

### 3D Hero Section

![3D Hero](docs/images/hero-3d.png)
_Interactive 3D brain visualization with floating particles_

### Resume Analysis Dashboard

![Dashboard](docs/images/dashboard.png)
_Comprehensive analysis with match scores and skill gaps_

### Interview Preparation

![Interview Prep](docs/images/interview.png)
_AI-generated questions tailored to your background_

### Career Analytics

![Analytics](docs/images/analytics.png)
_Industry trends and skill demand insights_

</details>

## 🎯 Usage Guide

### 1. Resume Upload & Analysis

```typescript
// Upload resume (PDF, DOC, DOCX, TXT)
const resumeFile = new File([...], 'resume.pdf');

// Paste job description
const jobDescription = `
Software Engineer - Microsoft
Requirements: React, TypeScript, Azure, Node.js...
`;

// Get AI analysis
const analysis = await analyzeResume(resumeFile, jobDescription);
```

### 2. Skill Gap Analysis

The AI analyzes your resume against job requirements and provides:

- **Match Score**: Percentage compatibility (0-100%)
- **Present Skills**: Technologies and competencies you have
- **Missing Skills**: Critical gaps to address
- **Learning Path**: Recommended courses and timeline
- **Salary Estimate**: Market-based compensation range

### 3. Interview Preparation

Generate customized questions based on:

- **Your Background**: Projects, experience, and skills
- **Target Role**: Specific job requirements and level
- **Question Types**: Technical, behavioral, and situational
- **Difficulty Levels**: Progressive complexity

### 4. Resume Enhancement

AI-powered suggestions for:

- **Impact Statements**: Quantified achievements
- **Keyword Optimization**: ATS-friendly formatting
- **Skill Highlighting**: Relevant technology emphasis
- **Experience Framing**: Better bullet point structure

## 🛠️ Development

### Local Development Setup

```bash
# Start frontend development server
cd app/frontend
npm install
npm run dev  # Runs on http://localhost:5173

# Start backend with hot reload
cd app/backend
pip install -r requirements.txt
python -m flask run --host 0.0.0.0 --port 8000 --debug

# Or use gunicorn for production-like environment
gunicorn --bind=0.0.0.0:8000 --workers=2 --threads=4 app:app
```

### Environment Variables

Create `.env` files for local development:

**Frontend (.env.local):**

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
```

**Backend (.env):**

```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHATGPT_DEPLOYMENT=gpt-35-turbo
AZURE_OPENAI_CHATGPT_MODEL=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-02-01
```

### Code Quality

```bash
# Frontend linting and formatting
npm run lint
npm run format

# Backend code quality
python -m black .
python -m isort .
python -m flake8
```

## 📊 Cost Optimization

### Azure Resource Costs (Monthly Estimates)

| Service            | Tier        | Cost (USD)  | Usage                    |
| ------------------ | ----------- | ----------- | ------------------------ |
| Azure App Service  | B1 Basic    | ~$13        | Web hosting (Always On)  |
| Azure OpenAI       | Pay-per-use | ~$2-10      | API calls (GPT-3.5-Turbo)|
| **Total**          |             | **~$15-23** | **Light-moderate usage** |

### Cost Optimization Features (Built-in)

1. ✅ **GPT-3.5-Turbo** - 10-15x cheaper than GPT-4
2. ✅ **Response Caching** - 1-hour cache for repeat queries ($0.00 cost!)
3. ✅ **Rate Limiting** - 10 req/min, 50 req/hour per IP
4. ✅ **Reduced Token Limits** - Optimized for cost without quality loss
5. ✅ **Always On** - Eliminates cold start delays (B1 tier)

See [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) for detailed cost analysis.

## 🔧 Configuration

### Customizing AI Behavior

Modify system prompts in `app/backend/services/ai_service.py`:

```python
system_prompt = """You are an expert AI Career Navigator specializing in tech careers.
[Customize behavior, tone, and expertise areas]
"""
```

### Adding New Analysis Features

1. **Frontend**: Add new components in `app/frontend/src/components/`
2. **Backend**: Add new routes in `app/backend/routes/api_routes.py`
3. **Services**: Extend AI service in `app/backend/services/ai_service.py`

### Styling and Themes

Customize design in `app/frontend/tailwind.config.js`:

```javascript
module.exports = {
	theme: {
		extend: {
			colors: {
				primary: {
					/* Your brand colors */
				},
				accent: {
					/* Accent colors */
				},
			},
			animation: {
				"custom-float": "float 3s ease-in-out infinite",
			},
		},
	},
};
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **TypeScript** for type safety
- **ESLint + Prettier** for consistent formatting
- **Conventional Commits** for clear commit messages
- **Test coverage** for new features

## 📈 Roadmap

### Q1 2024

- [ ] **Multi-language Support** (Spanish, French, German)
- [ ] **LinkedIn Integration** for automatic profile sync
- [ ] **Video Interview Practice** with AI feedback
- [ ] **Career Path Visualization** with interactive timelines

### Q2 2024

- [ ] **Company-specific Analysis** (FAANG, startups, etc.)
- [ ] **Peer Comparison** and benchmarking
- [ ] **Mobile App** (React Native)
- [ ] **Advanced Analytics** with ML insights

### Q3 2024

- [ ] **AI Mock Interviews** with voice interaction
- [ ] **Portfolio Builder** with AI assistance
- [ ] **Job Matching** with real-time opportunities
- [ ] **Mentorship Connections** based on career goals

## 🔍 Troubleshooting

### Common Issues

**Azure OpenAI Connection:**

```bash
# Verify credentials
azd env get-values | grep OPENAI

# Test connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  "$OPENAI_ENDPOINT/openai/models?api-version=2023-12-01-preview"
```

**Frontend Build Issues:**

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 20+
```

**Backend Dependencies:**

```bash
# Reinstall Python packages
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

### Performance Optimization

1. **Enable caching** for repeated analyses
2. **Compress images** and assets
3. **Use CDN** for static content
4. **Implement pagination** for large datasets

## 📞 Support

- **Live Demo**: [ai-career-navigator-backend.azurewebsites.net](https://ai-career-navigator-backend.azurewebsites.net)
- **Issues**: [GitHub Issues](https://github.com/Aryanjstar/AI-Career-Navigator/issues)
- **Email**: aryanjstar3@gmail.com
- **LinkedIn**: [Aryan Jaiswal](https://www.linkedin.com/in/aryanjstar/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Azure OpenAI Team** for powerful AI capabilities
- **React Three Fiber** community for 3D web development
- **Tailwind Labs** for outstanding CSS framework
- **Open Source Contributors** who make projects like this possible

## 🌟 Show Your Support

If this project helps you land your dream job, please ⭐ star this repository and share it with others!

---

**Built with ❤️ for the developer community**

_Empowering careers through AI innovation_
