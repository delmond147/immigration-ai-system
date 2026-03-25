# 🏛️ Immigration Law Firm AI Automation System

A production-ready AI automation system built for immigration law firms.
Eliminates repetitive tasks through intelligent automation and a 24/7 AI assistant.

## 🚀 Live Demo

[View Live Demo](https://immigration-ai-system-v1.streamlit.app/)

## 🎯 What It Does

### 1. Client Intake Automation

- Client fills intake form → CRM updated instantly
- Personalized welcome email sent automatically
- Zero manual work required

### 2. 24/7 AI Agent with RAG

- Answers immigration questions around the clock
- Trained on firm's own documents via RAG pipeline
- Logs every conversation to CRM automatically

### 3. Consultation Follow-Up Sequences

- Reminder emails 24 hours before consultations
- Follow-up emails after consultations
- Reactivation emails for cold leads

### 4. Document Checklist Automation

- Detects client case type automatically
- Sends correct document checklist by email
- Tracks document submission status

### 5. Beautiful Chat UI

- Professional client-facing interface
- PDF upload to expand knowledge base
- Real-time conversation with AI agent

## 🛠️ Tech Stack

| Layer           | Technology                 |
| --------------- | -------------------------- |
| Language        | Python 3.10+               |
| AI Model        | Groq API (LLaMA 3.3 70B)   |
| RAG Pipeline    | LangChain + FAISS + TF-IDF |
| Database/CRM    | Airtable                   |
| Backend         | FastAPI                    |
| Frontend        | Streamlit                  |
| Email           | Resend                     |
| Forms           | Tally.so                   |
| Package Manager | uv                         |

## 📁 Project Structure

```
immigration-ai-system/
├── app.py                          # Streamlit UI
├── main.py                         # CLI entry point
├── knowledge_base/                 # Firm documents
├── src/
│   ├── agent/
│   │   ├── immigration_agent.py    # AI agent
│   │   └── knowledge_base.py       # RAG pipeline
│   ├── automations/
│   │   ├── followup.py             # Follow-up sequences
│   │   ├── document_checklist.py   # Checklist automation
│   │   └── checklists.py           # Document templates
│   ├── database/
│   │   └── airtable_client.py      # Airtable connection
│   ├── email_service/
│   │   └── mailer.py               # Email templates
│   └── intake/
│       └── webhook.py              # FastAPI webhook
└── .env                            # API keys (not in repo)
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/immigration-ai-system.git
cd immigration-ai-system
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file:

```
GROQ_API_KEY=your-groq-key
AIRTABLE_API_KEY=your-airtable-key
AIRTABLE_BASE_ID=your-base-id
RESEND_API_KEY=your-resend-key
```

### 4. Run the Streamlit UI

```bash
uv run streamlit run app.py
```

### 5. Run the webhook server

```bash
uvicorn src.intake.webhook:app --reload --port 8000
```

## 🔧 Environment Variables

| Variable           | Description                    |
| ------------------ | ------------------------------ |
| `GROQ_API_KEY`     | Groq API key for LLM           |
| `AIRTABLE_API_KEY` | Airtable personal access token |
| `AIRTABLE_BASE_ID` | Airtable base ID               |
| `RESEND_API_KEY`   | Resend API key for emails      |

## 📊 Use Cases

This system can be adapted for any professional services business:

- ⚖️ Law firms
- 🏥 Medical practices
- 🏠 Real estate agencies
- 💼 Consulting firms
- 📊 Accounting practices

## 👨‍💻 Built By: Delmond Bongha

Built as a portfolio project demonstrating end-to-end AI automation
development using Python, LangChain, and modern AI tools.
