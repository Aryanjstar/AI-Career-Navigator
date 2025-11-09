# AI Career Navigator

An intelligent career guidance platform powered by Azure OpenAI that provides personalized career advice, resume analysis, interview preparation, and skill gap assessment.

## Features

- **Career Chat**: Interactive AI-powered career guidance with personalized recommendations
- **Resume Analysis**: Comprehensive resume review with ATS optimization suggestions
- **Interview Preparation**: Tailored interview questions and preparation strategies
- **Skill Gap Analysis**: Identify missing skills and get structured learning roadmaps

## Tech Stack

- **Backend**: Python, Flask, Azure OpenAI
- **Frontend**: HTML, CSS, JavaScript (Tailwind CSS)
- **Deployment**: Azure App Service, Render, Netlify

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r app/backend/requirements.txt`
3. Set environment variables:
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_KEY`
4. Run: `python app/backend/app.py`

## Deployment

The application can be deployed on Azure, Render, or Netlify. See `render.yaml` for Render deployment configuration.

## License

MIT
