# 📋 GitHub Commit Guidelines - AI Career Navigator

## ✅ WHAT TO COMMIT

### 📁 Source Code Files
```
✅ frontend/src/           # React TypeScript components
✅ backend/               # Python FastAPI backend
✅ *.ts, *.tsx, *.js     # TypeScript/JavaScript files
✅ *.py                  # Python source files
✅ *.css, *.scss         # Stylesheets
```

### 📄 Configuration Templates
```
✅ package.json          # Dependencies and scripts
✅ requirements.txt      # Python dependencies
✅ tsconfig.json        # TypeScript configuration
✅ tailwind.config.js   # Tailwind CSS config
✅ vite.config.ts       # Vite build configuration
✅ azure.yaml           # Azure Developer CLI config
✅ .env.example         # Environment variable template
```

### 📚 Documentation
```
✅ README.md            # Main project documentation
✅ CONTRIBUTING.md      # Contribution guidelines
✅ LICENSE              # MIT license
✅ docs/                # Additional documentation
✅ PROJECT_SUBMISSION.md # Build-a-thon submission
✅ SECURITY_GUIDELINES.md # Security best practices
```

### 🔧 Development Tools
```
✅ .gitignore           # Git exclusions
✅ .github/workflows/   # GitHub Actions
✅ Dockerfile          # Container configuration
✅ docker-compose.yml  # Multi-container setup
```

### 🧪 Testing Files
```
✅ tests/               # Test files
✅ *.test.ts           # Unit tests
✅ *.test.py           # Python tests
✅ jest.config.js      # Jest configuration
✅ pytest.ini          # Pytest configuration
```

---

## 🚫 WHAT NOT TO COMMIT

### 🔐 Sensitive Data (CRITICAL!)
```
❌ .env                # Environment variables
❌ .env.local          # Local environment config
❌ .env.production     # Production secrets
❌ *.env               # Any environment files
❌ secrets/            # Secret files directory
❌ config/secrets.json # Secret configuration
```

### 🔑 API Keys & Credentials
```
❌ AZURE_OPENAI_API_KEY        # OpenAI API key
❌ AZURE_SEARCH_API_KEY        # Search service key
❌ AZURE_STORAGE_CONNECTION_STRING # Storage credentials
❌ Any *_SECRET or *_PASSWORD variables
❌ Database connection strings with passwords
❌ JWT secrets or encryption keys
```

### ☁️ Azure Developer CLI Files
```
❌ .azd/               # Azure CLI working directory
❌ azd-*.json          # Azure deployment configs
❌ *.azd.env           # Azure environment files
❌ azure.yaml.backup   # Backup configurations
```

### 📂 Generated & Temporary Files
```
❌ node_modules/       # Node.js dependencies
❌ __pycache__/        # Python cache
❌ *.pyc               # Compiled Python
❌ dist/               # Build output
❌ build/              # Build artifacts
❌ .cache/             # Cache directories
❌ .tmp/               # Temporary files
❌ *.log               # Log files
```

### 🗄️ Databases & User Data
```
❌ *.db                # Database files
❌ *.sqlite            # SQLite databases
❌ analytics.db        # Analytics database
❌ uploads/            # User uploaded files
❌ resumes/            # Resume files
❌ user_data/          # Personal user data
❌ temp_files/         # Temporary uploads
```

### 💻 IDE & OS Files
```
❌ .DS_Store           # macOS Finder info
❌ Thumbs.db           # Windows thumbnails
❌ .vscode/settings.json # VS Code settings (if personal)
❌ .idea/              # JetBrains IDE files
❌ *.swp, *.swo        # Vim swap files
❌ *~                  # Backup files
```

### 📊 Analytics & Logs
```
❌ logs/               # Application logs
❌ *.log               # Log files
❌ nohup.out          # Process output
❌ career_nav.log     # Application-specific logs
❌ debug.log          # Debug information
❌ error.log          # Error logs
```

---

## 🛡️ Security Checklist Before Committing

### 1. Environment Variables Check
```bash
# ✅ Verify no .env files are staged
git status | grep -E "\.env"

# ✅ Check for API keys in staged files
git diff --staged | grep -i "api.*key\|secret\|password"
```

### 2. File Content Scan
```bash
# ✅ Scan for sensitive patterns
grep -r "sk-" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "AZURE_OPENAI_API_KEY" . --exclude-dir=node_modules --exclude-dir=.git
```

### 3. Pre-commit Validation
```bash
# ✅ Use these commands before committing
git add .
git status                    # Review what's being committed
git diff --staged --name-only # See staged files
git diff --staged            # Review actual changes
```

---

## 🚀 Recommended Git Workflow

### 1. Initial Setup
```bash
# Clone your repository
git clone https://github.com/Aryanjstar/AI-Career-Navigator.git
cd AI-Career-Navigator

# Create environment file from template
cp .env.example .env.local
# Edit .env.local with your actual values (DON'T commit this!)
```

### 2. Before Each Commit
```bash
# Check status
git status

# Add files selectively (avoid adding everything with git add .)
git add README.md
git add frontend/src/
git add backend/

# Review what you're committing
git diff --staged

# Commit with descriptive message
git commit -m "feat: add 3D visualization component with Three.js"
```

### 3. Push to GitHub
```bash
# Push to your repository
git push origin main
```

---

## 🔍 Common Mistakes to Avoid

### ❌ DON'T DO THESE:
```bash
git add .                     # Adds everything, including secrets
git add -A                    # Same as above
git commit -am "quick fix"    # Commits without reviewing
```

### ✅ DO THESE INSTEAD:
```bash
git add frontend/src/         # Add specific directories
git add *.md                  # Add specific file types
git status                    # Always check before committing
git diff --staged            # Review changes before committing
```

---

## 📞 Emergency: If You Accidentally Commit Secrets

### 1. Immediate Action (if just committed)
```bash
# Remove from last commit
git reset HEAD~1
git status  # See what's now unstaged
# Remove sensitive files from staging
git restore .env
# Commit again without sensitive files
git add frontend/ backend/ *.md
git commit -m "fix: proper commit without secrets"
```

### 2. If Already Pushed to GitHub
```bash
# Force remove from history (USE WITH CAUTION!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (this rewrites history)
git push --force
```

### 3. Rotate All Compromised Secrets
- 🔄 Generate new Azure OpenAI API keys
- 🔄 Create new Azure Search service keys
- 🔄 Update storage account access keys
- 🔄 Regenerate any other exposed credentials

---

## 📝 Final Checklist Before Submission

- [ ] No `.env` files in repository
- [ ] No API keys in source code
- [ ] All secrets use environment variables
- [ ] `.gitignore` is comprehensive
- [ ] README is updated with correct URLs
- [ ] All personal information is removed
- [ ] Test data is excluded
- [ ] Build artifacts are ignored
- [ ] License and attribution are correct
- [ ] Documentation is complete

---

**🛡️ Remember: When in doubt, don't commit it!**

*Security is everyone's responsibility. Better to be safe than sorry.*
