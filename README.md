## <!--

<!-- lsof -i :8000 | grep LISTEN

kill 58453 58487 -->

name: RAG chat app with your data (Python)
description: Chat with your domain data using Azure OpenAI and Azure AI Search.
languages:

- python
- typescript
- bicep
- azdeveloper
products:
- azure-openai
- azure-cognitive-search
- azure-app-service
- azure
page_type: sample
urlFragment: azure-search-openai-demo

---

-->

# 🎯 AI Career Navigator

[![Azure](https://img.shields.io/badge/Azure-OpenAI-blue.svg)](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Transform your career with AI-powered resume analysis, skill gap identification, and personalized interview preparation.**

A modern, full-stack web application that revolutionizes career development through advanced AI technologies. Built with Azure OpenAI, React, and cutting-edge 3D visualizations.

![AI Career Navigator Demo](docs/images/hero-demo.png)

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

- **Python 3.11** with FastAPI for high-performance APIs
- **Azure OpenAI Service** with GPT-4 for intelligent analysis
- **Azure AI Search** for document indexing and retrieval
- **Azure Blob Storage** for secure file storage
- **PostgreSQL** for structured data persistence

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
git clone https://github.com/your-username/ai-career-navigator.git
cd ai-career-navigator

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
npm run dev  # Frontend on http://localhost:3000
python -m uvicorn app:app --reload  # Backend on http://localhost:8000
```

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
npm run dev

# Start backend with hot reload
cd app/backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Run tests
npm test                    # Frontend tests
python -m pytest          # Backend tests
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
OPENAI_API_KEY=your-api-key
OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_SEARCH_SERVICE=your-search-service
AZURE_SEARCH_INDEX=your-index
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
| Azure App Service  | B1 Basic    | ~$13        | Web hosting              |
| Azure OpenAI       | Pay-per-use | ~$30-50     | API calls                |
| Azure AI Search    | Basic       | ~$25        | Document indexing        |
| Azure Blob Storage | Standard    | ~$5         | File storage             |
| **Total**          |             | **~$73-93** | **Light-moderate usage** |

### Cost Reduction Tips

1. **Use Azure Free Tier** when possible
2. **Optimize OpenAI calls** with caching and batching
3. **Scale down during low usage** periods
4. **Monitor usage** with Azure Cost Management

## 🔧 Configuration

### Customizing AI Behavior

Modify system prompts in `app/backend/approaches/chatreadretrieveread.py`:

```python
SYSTEM_MESSAGE_CHAT_CONVERSATION = """
You are an AI Career Navigator assistant...
[Customize behavior, tone, and expertise areas]
"""
```

### Adding New Analysis Features

1. **Frontend**: Add new components in `app/frontend/src/components/`
2. **Backend**: Extend approaches in `app/backend/approaches/`
3. **Data**: Add training content in `data/` directory

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

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/ai-career-navigator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/ai-career-navigator/discussions)
- **Email**: support@ai-career-navigator.com

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
