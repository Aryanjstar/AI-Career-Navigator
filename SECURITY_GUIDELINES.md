# 🚨 What NOT to Commit to GitHub - Security Guidelines

## 🔒 Critical Security Information

**NEVER commit these files or information to your GitHub repository!**

## 🚫 Sensitive Files & Data

### 1. **Environment Variables & Configuration**
```
❌ .env
❌ .env.local
❌ .env.production
❌ .env.development
❌ .env.staging
❌ *.env
❌ config/secrets.json
❌ local.settings.json
```

### 2. **API Keys & Secrets**
```
❌ AZURE_OPENAI_API_KEY
❌ AZURE_SEARCH_API_KEY
❌ AZURE_STORAGE_CONNECTION_STRING
❌ Any *_SECRET or *_PASSWORD variables
❌ Database connection strings with credentials
❌ JWT secrets or encryption keys
```

### 3. **Azure Developer CLI Files**
```
❌ .azd/
❌ azd-*.json
❌ *.azd.env
❌ azure.yaml.backup
```

### 4. **Certificates & Keys**
```
❌ *.key
❌ *.pem
❌ *.p12
❌ *.pfx
❌ *.crt (private certificates)
❌ ssh_keys/
```

### 5. **Database Files**
```
❌ *.db
❌ *.sqlite
❌ *.sqlite3
❌ analytics.db
❌ career_navigator.db
❌ Database dumps with sensitive data
```

### 6. **User Data & Uploads**
```
❌ uploads/
❌ user_data/
❌ resumes/
❌ temp_files/
❌ processed_files/
❌ Any folder containing user-uploaded content
```

### 7. **Log Files with Sensitive Data**
```
❌ *.log (if containing API keys or user data)
❌ debug.log
❌ error.log (if containing sensitive info)
❌ nohup.out
❌ career_nav.log
```

### 8. **IDE & System Files**
```
❌ .DS_Store (macOS)
❌ Thumbs.db (Windows)
❌ *.tmp, *.temp
❌ *~ (backup files)
❌ .vscode/settings.json (if containing secrets)
```

### 9. **Node.js & Python Artifacts**
```
❌ node_modules/
❌ __pycache__/
❌ *.pyc
❌ .pytest_cache/
❌ coverage/
❌ dist/ (build outputs)
```

### 10. **Backup & Archive Files**
```
❌ *.backup
❌ *.bak
❌ backup/
❌ *.tar.gz (if containing sensitive data)
❌ *.zip (if containing sensitive data)
```

## ✅ What TO Commit

### 1. **Configuration Templates**
```
✅ .env.example
✅ .env.template
✅ config.example.json
✅ azure.yaml.template
```

### 2. **Documentation**
```
✅ README.md
✅ CONTRIBUTING.md
✅ LICENSE
✅ docs/
✅ DEPLOYMENT.md
```

### 3. **Source Code**
```
✅ src/
✅ frontend/src/
✅ backend/
✅ *.ts, *.tsx, *.js, *.jsx
✅ *.py
✅ *.css, *.scss
```

### 4. **Configuration Files (without secrets)**
```
✅ package.json
✅ tsconfig.json
✅ tailwind.config.js
✅ vite.config.ts
✅ requirements.txt
✅ azure.yaml (template)
```

### 5. **CI/CD & Deployment**
```
✅ .github/workflows/
✅ Dockerfile
✅ docker-compose.yml
✅ .dockerignore
```

### 6. **Testing**
```
✅ tests/
✅ *.test.ts
✅ *.test.py
✅ jest.config.js
✅ pytest.ini
```

## 🛡️ How to Secure Your Repository

### 1. **Use Environment Variables**
```bash
# Instead of hardcoding secrets
const apiKey = "sk-1234567890abcdef"; // ❌ NEVER DO THIS

# Use environment variables
const apiKey = process.env.AZURE_OPENAI_API_KEY; // ✅ CORRECT
```

### 2. **Azure Key Vault Integration**
```python
# Store secrets in Azure Key Vault
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
api_key = client.get_secret("azure-openai-api-key").value
```

### 3. **Use .gitignore Properly**
```bash
# Your .gitignore should include:
.env
*.env
.azd/
secrets/
*.key
uploads/
__pycache__/
node_modules/
```

### 4. **Template Files for Onboarding**
```bash
# Create template files for new developers
cp .env .env.example
# Edit .env.example to remove actual values
```

## 🚨 If You Accidentally Commit Secrets

### 1. **Immediate Actions**
```bash
# Remove the file from tracking
git rm --cached .env

# Commit the removal
git commit -m "Remove accidentally committed .env file"

# Force push to rewrite history (if recent)
git push --force
```

### 2. **For Older Commits**
```bash
# Use git filter-branch or BFG Repo-Cleaner
# to remove files from entire history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### 3. **Rotate All Compromised Secrets**
- 🔄 Generate new API keys
- 🔄 Update Azure resource access keys
- 🔄 Change database passwords
- 🔄 Regenerate certificates

## 📋 Pre-Commit Checklist

Before every commit, verify:

- [ ] No `.env` files in staged changes
- [ ] No API keys in code
- [ ] No database credentials
- [ ] No user data or uploads
- [ ] No log files with sensitive info
- [ ] Only template/example config files
- [ ] All secrets using environment variables

## 🔍 Automated Security Scanning

### GitHub Security Features
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: detect-private-key
      - id: check-merge-conflict
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
EOF

# Install hooks
pre-commit install
```

## 📞 Security Support

If you suspect a security issue:

- 🔒 **Private Security Report**: [aryanjstar@gmail.com](mailto:aryanjstar@gmail.com)
- 🐛 **General Issues**: [GitHub Issues](https://github.com/Aryanjstar/AI-Career-Navigator/issues)
- 📚 **Documentation**: [Security Guidelines](docs/SECURITY.md)

---

**🛡️ Remember: Security is everyone's responsibility!**

*When in doubt, don't commit it. Better safe than sorry.*
