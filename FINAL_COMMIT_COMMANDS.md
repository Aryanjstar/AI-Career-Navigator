# 🚀 Final GitHub Commit Commands - AI Career Navigator

## 📋 Pre-Commit Security Check

Before committing, run these safety checks:

```bash
# 1. Check what files will be committed
git status

# 2. Scan for any accidentally staged sensitive files
git ls-files | grep -E "\.env$|\.env\.|secrets|\.key$|\.pem$"

# 3. Search for API keys in staged content
git diff --staged | grep -i "api.*key\|secret\|password\|sk-"

# 4. Verify .gitignore is working
ls -la | grep -E "\.env|\.azd|node_modules|__pycache__"
```

## 🎯 Final Commit Commands

Execute these commands in sequence:

```bash
# 1. Initialize git repository (if not already done)
git init

# 2. Add remote origin
git remote add origin https://github.com/Aryanjstar/AI-Career-Navigator.git

# 3. Set main as default branch
git branch -M main

# 4. Add files to staging (CAREFULLY - exclude sensitive files)
git add README.md
git add CONTRIBUTING.md
git add LICENSE
git add PROJECT_SUBMISSION.md
git add SECURITY_GUIDELINES.md
git add COMMIT_GUIDELINES.md
git add package.json
git add azure.yaml
git add .gitignore
git add frontend/
git add backend/
git add docs/

# 5. Verify what's being committed
git status
echo "📝 Review the above files - ensure no .env files or secrets!"

# 6. Create initial commit
git commit -m "feat: initial commit - AI Career Navigator with Azure OpenAI integration

- Complete React TypeScript frontend with 3D visualizations
- FastAPI Python backend with Azure OpenAI integration
- Comprehensive documentation and deployment guides
- Production-ready Azure Developer CLI configuration
- Security guidelines and contribution documentation"

# 7. Push to GitHub
git push -u origin main
```

## ⚠️ CRITICAL: Files to NEVER Commit

Make sure these are NOT in your staging area:

```bash
# These should return nothing or be in .gitignore
git ls-files | grep -E "\.env$|\.env\."
git ls-files | grep -E "\.azd/"
git ls-files | grep -E "node_modules"
git ls-files | grep -E "__pycache__"
git ls-files | grep -E "secrets"
git ls-files | grep -E "\.key$|\.pem$"
```

## 🔒 Security Verification Commands

Run these to ensure no secrets are committed:

```bash
# Check for API keys in committed content
git log --all --full-history -- "**/.*" | grep -i "api.*key\|secret"

# Verify sensitive directories are ignored
ls -la | grep -E "\.env|\.azd|uploads|logs"

# Check .gitignore is working
git check-ignore .env
git check-ignore .azd/
git check-ignore node_modules/
git check-ignore __pycache__/
```

## 🎉 Post-Commit Actions

After successful push:

```bash
# 1. Verify remote repository
git remote -v

# 2. Check branch status
git branch -a

# 3. View commit history
git log --oneline -5

# 4. Confirm GitHub repository
echo "🌐 Visit: https://github.com/Aryanjstar/AI-Career-Navigator"
echo "📋 Submit for Build-a-thon using PROJECT_SUBMISSION.md"
```

## 🚨 If Something Goes Wrong

### Uncommit if you made a mistake:
```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Remove files from staging
git restore --staged filename

# Re-add correct files and commit again
```

### Remove accidentally committed secrets:
```bash
# Remove file from history (DANGEROUS - rewrites history)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (only if repository is not shared)
git push --force
```

## ✅ Success Indicators

You've successfully committed when:
- [ ] Git push completes without errors
- [ ] GitHub repository shows all your files
- [ ] No .env files visible in GitHub
- [ ] README.md renders correctly
- [ ] All links work in the repository

---

**🛡️ Remember: Security first! When in doubt, don't commit it.**
