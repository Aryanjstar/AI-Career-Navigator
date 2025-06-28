# Contributing to AI Career Navigator

First off, thank you for considering contributing to AI Career Navigator! 🎉

It's people like you that make this platform a great tool for career development.

## 🌟 Ways to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues as you might find that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include screenshots if possible**
- **Mention your browser, OS, and versions**

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the expected behavior**
- **Explain why this enhancement would be useful**

### 🛠️ Code Contributions

#### Development Process

1. Fork the repository
2. Create a new branch from `main`
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request

#### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Install dependencies
npm install
cd backend && pip install -r requirements.txt

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development servers
npm run dev:all
```

#### Coding Standards

**Frontend (TypeScript/React):**
- Use TypeScript for all new code
- Follow React Hooks patterns
- Use functional components
- Write meaningful variable and function names
- Add JSDoc comments for complex functions

**Backend (Python):**
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Use async/await for I/O operations
- Handle errors appropriately

**Testing:**
- Write unit tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test both happy path and error cases

#### Commit Message Format

We use Conventional Commits specification:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Examples:
```
feat(resume): add PDF parsing with tables support
fix(interview): resolve question generation timeout
docs(readme): update installation instructions
```

## 📋 Pull Request Process

1. **Update the README.md** with details of changes if applicable
2. **Update version numbers** in package.json and requirements.txt if applicable
3. **Ensure any install or build dependencies are removed** before the end of the layer when doing a build
4. **Increase the version numbers** in any examples files and the README.md to the new version that this Pull Request would represent
5. **Your PR will be merged** once you have the sign-off of at least one maintainer

## 🏷️ Issue and Pull Request Labels

We use labels to organize and prioritize issues and pull requests:

### Type Labels
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `question`: Further information is requested

### Priority Labels
- `priority: high`: Critical issues that need immediate attention
- `priority: medium`: Important issues that should be addressed soon
- `priority: low`: Nice to have improvements

### Status Labels
- `status: needs review`: Waiting for review from maintainers
- `status: in progress`: Currently being worked on
- `status: blocked`: Cannot proceed until blocker is resolved

### Difficulty Labels
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `difficulty: easy`: Can be completed in a few hours
- `difficulty: medium`: May take a day or two
- `difficulty: hard`: Complex issue that may take several days

## 🎯 Development Guidelines

### Frontend Development

#### Component Structure
```
src/components/FeatureName/
  ├── index.ts              # Export barrel
  ├── FeatureName.tsx       # Main component
  ├── FeatureName.test.tsx  # Unit tests
  ├── types.ts              # TypeScript types
  └── hooks/                # Custom hooks
      └── useFeature.ts
```

#### State Management
- Use React's built-in state for component-level state
- Use Context API for shared state across components
- Consider Zustand for complex global state

#### Styling
- Use Tailwind CSS for styling
- Create reusable component variants with `class-variance-authority`
- Follow mobile-first responsive design

### Backend Development

#### API Structure
```
backend/
  ├── api/                  # API routes
  ├── core/                 # Core business logic
  ├── models/               # Data models
  ├── services/             # External service integrations
  ├── tests/                # Test files
  └── utils/                # Utility functions
```

#### Error Handling
```python
from fastapi import HTTPException, status

async def get_user_analysis(user_id: str):
    try:
        analysis = await analysis_service.get_analysis(user_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        return analysis
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
```

## 🧪 Testing

### Frontend Testing
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

### Backend Testing
```bash
# Run unit tests
python -m pytest

# Run with coverage
python -m pytest --cov=app

# Run specific test file
python -m pytest tests/test_analysis.py

# Run integration tests
python -m pytest tests/integration/
```

## 📚 Documentation

### Code Documentation
- Use JSDoc for TypeScript functions
- Use docstrings for Python functions
- Include examples in documentation
- Keep documentation up to date with code changes

### User Documentation
- Update README.md for new features
- Add screenshots for UI changes
- Create or update user guides in the `docs/` directory
- Update API documentation for backend changes

## 🎉 Recognition

Contributors will be added to our [Contributors](https://github.com/your-username/ai-career-navigator/graphs/contributors) page and mentioned in release notes.

### Contribution Levels
- 🥇 **Gold Contributors**: 5+ significant contributions
- 🥈 **Silver Contributors**: 3+ contributions
- 🥉 **Bronze Contributors**: 1+ contribution

## 📞 Getting Help

If you need help with anything, don't hesitate to reach out:

- 💬 [GitHub Discussions](https://github.com/Aryanjstar/AI-Career-Navigator/discussions)
- 📧 Email: [aryanjstar@gmail.com](mailto:aryanjstar@gmail.com)
- 🐛 [Create an Issue](https://github.com/Aryanjstar/AI-Career-Navigator/issues/new)

## 🤝 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

---

Thank you for contributing to AI Career Navigator! 🚀
