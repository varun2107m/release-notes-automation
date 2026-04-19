# 🚀 Release Notes Automation System

A Streamlit-based automation tool that generates and fetches release notes from Confluence and helps streamline product release communication across stakeholders.

---

## 📌 Features

- 🔄 Fetch release notes from Confluence pages
- 🧠 Automate release note generation from structured data (Jira / sheets / APIs)
- 📊 Clean UI using Streamlit for easy interaction
- 📧 Ready for email distribution to stakeholders
- 🔐 Secure API-based integration with Confluence
- ⚡ Fast and lightweight automation workflow

---

## 🏗️ Project Structure

release-notes-automation/
│
├── app.py # Streamlit entry point
├── fetch_confluence.py # Confluence API integration
├── requirements.txt # Dependencies
├── .gitignore # Ignored files
└── venv/ # Virtual environment (not committed)


---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/release-notes-automation.git
cd release-notes-automation

python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt

CONFLUENCE_BASE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_EMAIL=your-email@company.com
CONFLUENCE_API_TOKEN=your-api-token

streamlit run app.py

