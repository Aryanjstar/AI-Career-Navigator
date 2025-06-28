# 🔧 Development Guide

Comprehensive guide for contributing to and developing AI Career Navigator.

## 🚀 Quick Start for Developers

### Prerequisites
- **Node.js 20+** and npm
- **Python 3.11+** and pip
- **Git** with SSH keys configured
- **Docker** and **Docker Compose** (optional but recommended)
- **VS Code** with recommended extensions

### Development Setup

```bash
# 1. Fork and clone the repository
git clone git@github.com:YOUR_USERNAME/AI-Career-Navigator.git
cd AI-Career-Navigator

# 2. Set up development environment
make setup-dev  # Installs all dependencies and sets up pre-commit hooks

# 3. Copy environment templates
cp .env.example .env
cp frontend/.env.example frontend/.env.local

# 4. Start development services
make dev  # Starts all services in development mode
```

### Development Workflow

```bash
# Start development with hot reloading
make dev

# Run tests
make test

# Run linting and formatting
make lint
make format

# Build for production
make build

# Run end-to-end tests
make test-e2e
```

## 🏗️ Project Structure

```
AI-Career-Navigator/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Route components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── store/          # Zustand state management
│   │   ├── services/       # API service layer
│   │   ├── utils/          # Utility functions
│   │   └── types/          # TypeScript definitions
│   ├── public/             # Static assets
│   ├── tests/              # Frontend tests
│   └── package.json
├── backend/                  # FastAPI Python backend
│   ├── api/                # API route handlers
│   ├── services/           # Business logic
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── core/               # Core utilities
│   ├── approaches/         # AI prompt strategies
│   ├── tests/              # Backend tests
│   └── requirements.txt
├── docs/                    # Documentation
├── scripts/                 # Development scripts
├── .github/                 # GitHub Actions workflows
├── docker-compose.yml       # Local development services
├── Makefile                 # Development commands
└── README.md
```

## 🔧 Frontend Development

### Technology Stack
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Router** for navigation
- **React Hook Form** for forms
- **Axios** for API calls
- **Three.js** for 3D visualizations

### Component Development

#### Creating New Components
```bash
# Use the component generator
npm run generate:component ComponentName

# This creates:
# src/components/ComponentName/
# ├── index.tsx
# ├── ComponentName.tsx
# ├── ComponentName.test.tsx
# ├── ComponentName.module.css
# └── types.ts
```

#### Component Structure
```typescript
// src/components/ExampleComponent/ExampleComponent.tsx
import React from 'react';
import { ExampleComponentProps } from './types';
import styles from './ExampleComponent.module.css';

export const ExampleComponent: React.FC<ExampleComponentProps> = ({
  title,
  onAction,
  children,
  className = ''
}) => {
  const handleClick = () => {
    onAction?.('example-action');
  };

  return (
    <div className={`${styles.container} ${className}`}>
      <h2 className={styles.title}>{title}</h2>
      {children}
      <button onClick={handleClick} className={styles.actionButton}>
        Action
      </button>
    </div>
  );
};

export default ExampleComponent;
```

#### Testing Components
```typescript
// src/components/ExampleComponent/ExampleComponent.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ExampleComponent } from './ExampleComponent';

describe('ExampleComponent', () => {
  it('renders with title', () => {
    render(<ExampleComponent title="Test Title" />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('calls onAction when button is clicked', () => {
    const mockOnAction = jest.fn();
    render(<ExampleComponent title="Test" onAction={mockOnAction} />);
    
    fireEvent.click(screen.getByText('Action'));
    expect(mockOnAction).toHaveBeenCalledWith('example-action');
  });
});
```

### State Management with Zustand

```typescript
// src/store/resumeStore.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { Resume, AnalysisResult } from '../types';

interface ResumeState {
  // State
  currentResume: Resume | null;
  analysis: AnalysisResult | null;
  isAnalyzing: boolean;
  error: string | null;

  // Actions
  uploadResume: (file: File) => Promise<void>;
  analyzeResume: (jobDescription: string) => Promise<void>;
  clearAnalysis: () => void;
  setError: (error: string | null) => void;
}

export const useResumeStore = create<ResumeState>()(
  devtools(
    (set, get) => ({
      // Initial state
      currentResume: null,
      analysis: null,
      isAnalyzing: false,
      error: null,

      // Actions
      uploadResume: async (file: File) => {
        try {
          set({ isAnalyzing: true, error: null });
          const resume = await resumeService.upload(file);
          set({ currentResume: resume, isAnalyzing: false });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Upload failed',
            isAnalyzing: false 
          });
        }
      },

      analyzeResume: async (jobDescription: string) => {
        const { currentResume } = get();
        if (!currentResume) {
          set({ error: 'No resume uploaded' });
          return;
        }

        try {
          set({ isAnalyzing: true, error: null });
          const analysis = await resumeService.analyze(currentResume.id, jobDescription);
          set({ analysis, isAnalyzing: false });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Analysis failed',
            isAnalyzing: false 
          });
        }
      },

      clearAnalysis: () => set({ analysis: null, error: null }),
      setError: (error) => set({ error })
    }),
    { name: 'resume-store' }
  )
);
```

### API Service Layer

```typescript
// src/services/resumeService.ts
import { apiClient } from './apiClient';
import { Resume, AnalysisResult, UploadResponse } from '../types';

class ResumeService {
  async upload(file: File): Promise<Resume> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<UploadResponse>(
      '/api/resumes/upload',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000 // 30 second timeout for file uploads
      }
    );

    return response.data.resume;
  }

  async analyze(resumeId: string, jobDescription: string): Promise<AnalysisResult> {
    const response = await apiClient.post<AnalysisResult>(
      '/api/analysis/analyze',
      {
        resume_id: resumeId,
        job_description: jobDescription
      },
      { timeout: 60000 } // 60 second timeout for AI analysis
    );

    return response.data;
  }

  async getHistory(userId: string): Promise<Resume[]> {
    const response = await apiClient.get<Resume[]>(`/api/resumes/user/${userId}`);
    return response.data;
  }
}

export const resumeService = new ResumeService();
```

## ⚙️ Backend Development

### Technology Stack
- **FastAPI** with Python 3.11+
- **SQLAlchemy 2.0** for ORM
- **Alembic** for migrations
- **Pydantic** for data validation
- **Azure OpenAI** for AI services
- **PostgreSQL** for database
- **Redis** for caching
- **Pytest** for testing

### API Development

#### Creating New Endpoints
```python
# backend/api/resumes.py
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..core.security import get_current_user
from ..services.resume_service import ResumeService
from ..schemas.resume import ResumeCreate, ResumeResponse
from ..models.user import User

router = APIRouter(prefix="/api/resumes", tags=["resumes"])

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a resume file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF, DOC, DOCX, and TXT files are supported"
        )
    
    resume_service = ResumeService(db)
    resume = await resume_service.upload_resume(file, current_user.id)
    
    return ResumeResponse.from_orm(resume)

@router.get("/", response_model=List[ResumeResponse])
async def get_user_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for the current user."""
    resume_service = ResumeService(db)
    resumes = await resume_service.get_user_resumes(current_user.id)
    
    return [ResumeResponse.from_orm(resume) for resume in resumes]
```

#### Service Layer
```python
# backend/services/resume_service.py
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from typing import List, Optional
import hashlib
import uuid

from ..models.resume import Resume
from ..models.user import User
from ..core.storage import StorageService
from ..core.document_processor import DocumentProcessor

class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.storage = StorageService()
        self.processor = DocumentProcessor()
    
    async def upload_resume(self, file: UploadFile, user_id: str) -> Resume:
        """Upload and process a resume file."""
        # Read file content
        content = await file.read()
        content_hash = hashlib.sha256(content).hexdigest()
        
        # Check if this exact file was already uploaded
        existing_resume = self.db.query(Resume).filter(
            Resume.content_hash == content_hash,
            Resume.user_id == user_id
        ).first()
        
        if existing_resume:
            return existing_resume
        
        # Store file in blob storage
        file_url = await self.storage.upload_file(
            content=content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        # Process document content
        processed_content = await self.processor.extract_text(content, file.content_type)
        
        # Create database record
        resume = Resume(
            id=str(uuid.uuid4()),
            user_id=user_id,
            filename=file.filename,
            content_hash=content_hash,
            processed_content=processed_content,
            storage_url=file_url
        )
        
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        
        return resume
    
    async def get_user_resumes(self, user_id: str) -> List[Resume]:
        """Get all resumes for a user."""
        return self.db.query(Resume).filter(
            Resume.user_id == user_id
        ).order_by(Resume.created_at.desc()).all()
```

#### Database Models
```python
# backend/models/resume.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from ..core.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)
    processed_content = Column(Text)
    storage_url = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    analyses = relationship("AnalysisResult", back_populates="resume")
    
    def __repr__(self):
        return f"<Resume(id={self.id}, filename={self.filename})>"
```

#### Pydantic Schemas
```python
# backend/schemas/resume.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class ResumeBase(BaseModel):
    filename: str = Field(..., description="Original filename of the resume")

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: uuid.UUID
    user_id: uuid.UUID
    content_hash: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ResumeWithContent(ResumeResponse):
    processed_content: Optional[str] = None
```

### Testing

#### Unit Tests
```python
# backend/tests/test_resume_service.py
import pytest
from unittest.mock import Mock, AsyncMock
from fastapi import UploadFile
from io import BytesIO

from ..services.resume_service import ResumeService
from ..models.resume import Resume

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def resume_service(mock_db):
    return ResumeService(mock_db)

@pytest.mark.asyncio
async def test_upload_resume_success(resume_service, mock_db):
    # Arrange
    file_content = b"Test resume content"
    mock_file = UploadFile(
        filename="test_resume.pdf",
        file=BytesIO(file_content),
        content_type="application/pdf"
    )
    user_id = "test-user-id"
    
    mock_db.query.return_value.filter.return_value.first.return_value = None
    resume_service.storage.upload_file = AsyncMock(return_value="http://storage.url/file")
    resume_service.processor.extract_text = AsyncMock(return_value="Extracted text")
    
    # Act
    result = await resume_service.upload_resume(mock_file, user_id)
    
    # Assert
    assert isinstance(result, Resume)
    assert result.filename == "test_resume.pdf"
    assert result.user_id == user_id
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_upload_resume_duplicate(resume_service, mock_db):
    # Arrange
    existing_resume = Resume(id="existing-id", filename="test.pdf")
    mock_db.query.return_value.filter.return_value.first.return_value = existing_resume
    
    file_content = b"Test resume content"
    mock_file = UploadFile(
        filename="test_resume.pdf",
        file=BytesIO(file_content)
    )
    
    # Act
    result = await resume_service.upload_resume(mock_file, "user-id")
    
    # Assert
    assert result == existing_resume
    mock_db.add.assert_not_called()
```

#### Integration Tests
```python
# backend/tests/test_api_integration.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..core.database import get_db, Base
from ..core.security import get_current_user
from ..models.user import User

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return User(id="test-user-id", email="test@example.com", name="Test User")

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_upload_resume():
    # Arrange
    test_file_content = b"Test resume content"
    
    # Act
    response = client.post(
        "/api/resumes/upload",
        files={"file": ("test_resume.pdf", test_file_content, "application/pdf")}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_resume.pdf"
    assert "id" in data
    assert "created_at" in data

def test_get_user_resumes():
    # First upload a resume
    test_file_content = b"Test resume content"
    client.post(
        "/api/resumes/upload",
        files={"file": ("test_resume.pdf", test_file_content, "application/pdf")}
    )
    
    # Then get user resumes
    response = client.get("/api/resumes/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "test_resume.pdf"
```

## 🧪 Testing Strategy

### Frontend Testing
```bash
# Unit tests with Jest and React Testing Library
npm test

# Component tests
npm run test:components

# Integration tests
npm run test:integration

# End-to-end tests with Playwright
npm run test:e2e

# Coverage report
npm run test:coverage
```

### Backend Testing
```bash
# Unit tests
python -m pytest tests/unit/ -v

# Integration tests
python -m pytest tests/integration/ -v

# API tests
python -m pytest tests/api/ -v

# Coverage report
python -m pytest --cov=backend --cov-report=html
```

### Test Organization
```
tests/
├── frontend/
│   ├── components/          # Component unit tests
│   ├── hooks/              # Custom hook tests
│   ├── services/           # Service layer tests
│   ├── integration/        # Frontend integration tests
│   └── e2e/               # End-to-end tests
└── backend/
    ├── unit/               # Unit tests
    ├── integration/        # Integration tests
    ├── api/               # API endpoint tests
    └── fixtures/          # Test data and fixtures
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Run linting
        run: cd frontend && npm run lint
      
      - name: Run tests
        run: cd frontend && npm run test:ci
      
      - name: Build application
        run: cd frontend && npm run build

  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: cd backend && flake8 .
      
      - name: Run type checking
        run: cd backend && mypy .
      
      - name: Run tests
        run: cd backend && pytest -v --cov=. --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [frontend-tests, backend-tests]
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd frontend && npm ci
          npx playwright install
      
      - name: Start application
        run: |
          docker-compose up -d
          # Wait for services to be ready
          sleep 30
      
      - name: Run E2E tests
        run: cd frontend && npm run test:e2e
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-screenshots
          path: frontend/test-results/

  deploy:
    runs-on: ubuntu-latest
    needs: [frontend-tests, backend-tests, e2e-tests]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Azure CLI
        uses: azure/setup-azd@v0.1.0
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Azure
        run: azd deploy --no-prompt
        env:
          AZURE_ENV_NAME: production
```

## 📋 Code Standards

### TypeScript/JavaScript
- Use **TypeScript** for all new code
- Follow **ESLint** configuration
- Use **Prettier** for formatting
- Prefer **functional components** with hooks
- Use **strict null checks**
- Implement proper **error boundaries**

### Python
- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Implement **async/await** for I/O operations
- Use **Pydantic** for data validation
- Follow **SOLID principles**
- Write **docstrings** for all public functions

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/amazing-feature

# Make changes with good commit messages
git commit -m "feat: add resume analysis caching"

# Push and create PR
git push origin feature/amazing-feature

# Use conventional commit format
# feat: new feature
# fix: bug fix
# docs: documentation
# style: formatting
# refactor: code restructuring
# test: adding tests
# chore: maintenance
```

### Code Review Checklist
- [ ] **Functionality**: Does the code work as intended?
- [ ] **Tests**: Are there adequate tests with good coverage?
- [ ] **Performance**: Is the code efficient and optimized?
- [ ] **Security**: Are there any security vulnerabilities?
- [ ] **Documentation**: Is the code well-documented?
- [ ] **Standards**: Does it follow our coding standards?
- [ ] **Error Handling**: Are errors handled appropriately?

## 🚀 Deployment

### Local Development
```bash
# Start all services
make dev

# Individual services
make start-frontend    # http://localhost:5173
make start-backend     # http://localhost:8000
make start-db         # PostgreSQL on 5432
make start-redis      # Redis on 6379
```

### Staging Deployment
```bash
# Deploy to staging environment
azd deploy --environment staging

# Run staging tests
make test-staging
```

### Production Deployment
```bash
# Deploy to production
azd deploy --environment production

# Monitor deployment
azd monitor --follow
```

## 📚 Resources

### Learning Materials
- **React Documentation**: [react.dev](https://react.dev)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Azure OpenAI Guide**: [Azure OpenAI Docs](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- **TypeScript Handbook**: [typescriptlang.org](https://www.typescriptlang.org/docs/)

### Development Tools
- **VS Code Extensions**: ESLint, Prettier, Python, Thunder Client
- **Database Tools**: pgAdmin, DBeaver
- **API Testing**: Postman, Insomnia
- **Monitoring**: Azure Application Insights, Sentry

### Community
- **GitHub Discussions**: [Project Discussions](https://github.com/Aryanjstar/AI-Career-Navigator/discussions)
- **Discord**: Join our developer community
- **Office Hours**: Weekly developer Q&A sessions

---

**Happy coding! 🚀** 

For questions or help, reach out to the development team at [dev@ai-career-navigator.com](mailto:dev@ai-career-navigator.com)
