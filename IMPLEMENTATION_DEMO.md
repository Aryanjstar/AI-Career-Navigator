# 🚀 AI Career Navigator - Implementation Demo

## **1. Architecture Overview (5 minutes)**

### **Show the Project Structure**

```bash
# Run this in terminal to show project structure
tree -I 'node_modules|.venv|__pycache__|.git' -a
```

**Explain:**

- `build/career_navigator_pro.py` - Main application (2000+ lines)
- `app/frontend/` - React frontend (separate service)
- `app/backend/` - Python Flask API (separate service)
- `.env` - Azure OpenAI credentials
- `requirements.txt` - Python dependencies

---

## **2. Backend API Implementation (10 minutes)**

### **Show the Core Chat API**

```python
# Open: build/career_navigator_pro.py (lines 1823-1900)
@app.route('/api/career-chat', methods=['POST'])
def career_chat():
    """Handle career guidance chat"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_role = data.get('user_role', '')
        experience = data.get('experience', '')
        focus_area = data.get('focus_area', '')

        # Create contextual prompt for Azure OpenAI
        prompt = f"""
        **Act as an expert AI Career Mentor for the tech industry.**
        **User's Profile:**
        - **Current/Target Role:** {user_role}
        - **Experience Level:** {experience}
        - **Primary Goal:** {focus_area}
        **User's Question:** "{user_message}"
        """

        response = get_ai_response(prompt, max_tokens=1500)

        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Career chat error: {e}")
        return jsonify({"error": "Internal server error"}), 500
```

### **Show Azure OpenAI Integration**

```python
# Show the AI response function (lines 1760-1785)
def get_ai_response(prompt, max_tokens=2000):
    """Get response from Azure OpenAI"""
    if not client:
        return "Azure OpenAI client not configured properly."

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": """You are an expert AI Career Navigator..."""},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return f"I encountered an error processing your request."
```

---

## **3. Frontend Implementation (10 minutes)**

### **Show the Chat JavaScript**

```javascript
// Open: build/career_navigator_pro.py (lines 1246-1325)
async function sendMessage() {
	const messageInput = document.getElementById("user-message");
	const message = messageInput.value.trim();

	const userRole = document.getElementById("user-role").value;
	const experience = document.getElementById("user-experience").value;
	const focusArea = document.getElementById("focus-area").value;

	// Add user message to chat UI
	addMessage("user", message);

	try {
		const response = await fetch("/api/career-chat", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				message: message,
				user_role: userRole,
				experience: experience,
				focus_area: focusArea,
			}),
		});

		const data = await response.json();
		addMessage("ai", data.response);
	} catch (error) {
		addMessage("ai", `Connection error: ${error.message}`);
	}
}
```

### **Show the UI Creation**

```javascript
// Show addMessage function (lines 1327-1375)
function addMessage(sender, message) {
	const chatContainer = document.getElementById("chat-messages");
	const messageDiv = document.createElement("div");

	if (sender === "user") {
		messageDiv.innerHTML = `
            <div class="flex items-start space-x-3 justify-end">
                <div class="glass-card p-4 max-w-lg bg-blue-600/20 rounded-xl">
                    <p class="text-white">${escapedMessage}</p>
                </div>
                <div class="text-2xl">👤</div>
            </div>
        `;
	} else {
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
}
```

---

## **4. Configuration & Environment (5 minutes)**

### **Show Environment Setup**

```bash
# Show .env file
cat .env
```

```properties
AZURE_OPENAI_ENDPOINT=https://gpt-31.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_CHATGPT_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_CHATGPT_MODEL=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview
```

### **Show Dependencies**

```bash
# Show requirements.txt
head -20 requirements.txt
```

---

## **5. Advanced Features Demo (10 minutes)**

### **Show Resume Analysis API**

```python
# Lines 1903-1960
@app.route('/api/resume-analysis', methods=['POST'])
def resume_analysis():
    """Analyze resume for ATS optimization"""
    try:
        resume_text = ""

        # Handle file upload OR text input
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            if 'resume_file' in request.files:
                file = request.files['resume_file']
                resume_text = extract_text_from_file(file)
        else:
            data = request.get_json()
            resume_text = data.get('resume_text', '')

        # Create specialized prompt for resume analysis
        prompt = f"""
        **Act as an expert ATS (Applicant Tracking System) specialist...**
        **Resume Content:** {resume_text}
        """

        analysis = get_ai_response(prompt, max_tokens=2000)
        return jsonify({"response": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### **Show Interview Prep with Custom Tokens**

```python
# Lines 1961-2033 - Interview prep with 4000 tokens
@app.route('/api/interview-prep', methods=['POST'])
def interview_prep():
    """Generate interview questions and preparation tips"""
    try:
        data = request.get_json()
        role = data.get('role', '')
        target_company = data.get('target_company', '')
        company_size = data.get('company_size', '')

        prompt = f"""
        **Act as an experienced Interview Coach for '{target_company}'.**

        **Generate a complete interview preparation guide...**
        """

        # Note the higher token limit for comprehensive responses
        response_text = get_ai_response(prompt, max_tokens=4000)

        return jsonify({
            "response": response_text,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
```

---

### **6. **Show How to Add a New Feature** (15 minutes)**

```python
# Example: Add a new endpoint
@app.route('/api/salary-analysis', methods=['POST'])
def salary_analysis():
    """New feature: Salary analysis and negotiation tips"""
    try:
        data = request.get_json()
        role = data.get('role', '')
        location = data.get('location', '')
        experience = data.get('experience', '')

        prompt = f"""
        **Act as a Salary Negotiation Expert.**

        **Role:** {role}
        **Location:** {location}
        **Experience:** {experience}

        Provide salary insights and negotiation strategies.
        """

        response = get_ai_response(prompt, max_tokens=1000)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### **Add Frontend Support**

```javascript
// Add to the JavaScript section
async function analyzeSalary() {
	const role = document.getElementById("salary-role").value;
	const location = document.getElementById("salary-location").value;
	const experience = document.getElementById("salary-experience").value;

	try {
		const response = await fetch("/api/salary-analysis", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ role, location, experience }),
		});

		const data = await response.json();
		document.getElementById("salary-results").innerHTML = data.response;
	} catch (error) {
		console.error("Salary analysis error:", error);
	}
}
```

---

## **7. Deployment & Production (5 minutes)**

### **Show Start Script**

```bash
# Show app/start.sh
cat app/start.sh
```

### **Show How to Run**

```bash
# Simple deployment process
./app/start.sh

# Or manual steps:
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python build/career_navigator_pro.py
```

---

## **8. Key Implementation Highlights**

### **What Makes This Special:**

1. **Monolithic Architecture** - Everything in one file for simplicity
2. **Context-Aware AI** - User profile influences all responses
3. **Multiple Token Limits** - Different endpoints use different limits
4. **File Processing** - PDF and DOCX resume uploads
5. **Glassmorphism UI** - Modern design with backdrop filters
6. **Responsive Design** - Works on all device sizes
7. **Error Handling** - Comprehensive error management
8. **Azure OpenAI Integration** - Professional AI service

### **Technical Stack:**

- **Backend:** Python Flask + Azure OpenAI
- **Frontend:** Vanilla JavaScript + Tailwind CSS
- **Storage:** None (stateless)
- **Deployment:** Simple shell script
- **Security:** Environment variables for credentials

---

## **09. Demo Script (Total: 60 minutes)**

1. **Live Demo** (10 min) - Show the working app
2. **Architecture** (5 min) - Project structure
3. **Backend APIs** (15 min) - Core functionality
4. **Frontend Code** (10 min) - UI and interactions
5. **Configuration** (5 min) - Setup and deployment
6. **Advanced Features** (10 min) - Resume, Interview prep
7. **Q&A** (5 min) - Answer questions


