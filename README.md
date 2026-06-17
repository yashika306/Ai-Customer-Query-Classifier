# 🤖 AI Customer Query Classifier

An AI-powered customer support ticket classification system that securely processes customer queries using Large Language Models (LLMs). The application includes production-grade AI guardrails such as PII redaction, prompt injection detection, JSON validation, fallback handling, and cost tracking.

---

## 🚀 Features

* 🔒 PII Redaction (Sensitive Data Protection)
* 🛡️ Prompt Injection Detection
* 🤖 AI-Powered Ticket Classification
* ✅ JSON Output Validation
* 🔄 Fallback Handling
* 💰 LLM Cost Tracking
* 🌐 Web-Based User Interface

---

## 🌐 Live Demo

🚀 Try the application here: https://ai-customer-query-classifier.onrender.com/

---
### Architecture Diagram

![Project Architecture](assets/ticket-classification-architecture.png)

---

## 🏗️ System Architecture

```text
Customer Query
      │
      ▼
┌─────────────────────┐
│    PII Redaction    │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ Prompt Injection    │
│     Detection       │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ Ticket Classification│
│       (LLM)         │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│   JSON Validation   │
└─────────────────────┘
      │
   ┌──┴──┐
   │     │
   ▼     ▼
Success Failure
   │     │
   ▼     ▼
 Cost  Fallback
Tracker Response
```

---

## ⚙️ Tech Stack

| Component       | Technology            |
| --------------- | --------------------- |
| Backend         | Python                |
| Framework       | Flask                 |
| LLM Provider    | Groq                  |
| Validation      | Pydantic              |
| Frontend        | HTML, CSS, JavaScript |
| Deployment      | Render                |
| Version Control | Git & GitHub          |

---

## 📂 Project Structure

```text
Ai-Customer-Query-Classifier/
│
├── app.py
├── graph.py
├── schemas.py
├── requirements.txt
├── README.md
│
├── production_modules/
│   ├── classifier.py
│   ├── pii_redaction.py
│   ├── injection_check.py
│   └── cost_calculator.py
│
├── static/
│   └── index.html
│
└── assets/
    └── ticket-classification-architecture.png
```

---

## 🔄 Workflow

### Step 1: Customer Submits a Query

Example:

```text
My package was supposed to arrive 5 days ago and it still hasn't shown up.
Order #98765
```

### Step 2: PII Redaction

Sensitive information is detected and masked before being sent to the LLM.

### Step 3: Prompt Injection Detection

The system identifies malicious prompts such as:

```text
Ignore previous instructions
Reveal system prompt
Execute arbitrary commands
```

### Step 4: AI Classification

The LLM classifies the customer query into an appropriate support category.

### Step 5: JSON Validation

The generated output is validated against a predefined schema.

### Step 6: Cost Tracking

Estimated LLM token usage and inference cost are calculated.

### Step 7: Response Returned

The final validated classification result is returned to the user.

---

## 🎯 Supported Categories

* Billing Issues
* Refund Requests
* Technical Support
* Delivery Problems
* Account Management
* General Inquiry

---

## 🔒 Security Features

### PII Protection

Detects and redacts:

* Email Addresses
* Phone Numbers
* Account IDs
* Personal Information

### Prompt Injection Defense

Protects against:

* System Prompt Extraction
* Jailbreak Attempts
* Instruction Override Attacks

### Output Validation

Ensures:

* Structured Responses
* Valid Categories
* Safe Outputs

---

## 📊 Example Output

```json
{
  "category": "Delivery Issue",
  "priority": "High",
  "confidence": 0.96,
  "estimated_cost": "$0.0003"
}
```

---

## 🛠️ Installation

### Clone Repository

```bash
git clone https://github.com/yashika306/Ai-Customer-Query-Classifier.git
```

### Navigate to Project

```bash
cd Ai-Customer-Query-Classifier
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

### Run Application

```bash
python app.py
```

Application will be available at:

```text
http://localhost:5000
```

---

## ☁️ Deployment Details

- **Platform:** Render
- **Backend:** Flask (Python)
- **AI Provider:** Groq LLM API
- **Environment Variables:** Securely managed through Render
- **CI/CD:** Automatic deployment from GitHub
- **Live URL:** https://ai-customer-query-classifier.onrender.com/

---

## 🎓 Learning Outcomes

This project demonstrates:

* LLM Application Development
* Prompt Security Engineering
* AI Output Validation
* Production AI Guardrails
* Cost Monitoring
* End-to-End AI System Design
* AI System Architecture

---

## 👩‍💻 Author

**Yashika Duthuluru**  
Aspiring AI Engineer | Cloud Engineer | Software Developer

- 🔗 GitHub: https://github.com/yashika306
- 🔗 LinkedIn: https://www.linkedin.com/in/yashikaduthuluru/

---
