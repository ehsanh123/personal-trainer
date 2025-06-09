# 🤖 Async DialogflowCX Chatbot (FastAPI + JavaScript)

This project is a simple chatbot interface using **FastAPI** for the backend, **Google Dialogflow CX** for NLP, and **vanilla JavaScript** to create an interactive, async experience in the browser.

---

## 🚀 Features

- Asynchronous communication with Google Dialogflow CX
- Real-time status updates on the frontend ("Connecting", "Getting data", etc.)
- No page reloads — all handled via JS and `fetch()`
- Clean FastAPI project structure with template rendering

---

## 📁 Project Structure

project-root/ 

├── app2.py # Main FastAPI app 

├── templates/ 

│ └── index2.html # Jinja2 HTML template 

├── static/ 

│ └── script2.js # JS for handling async fetch and UI updates 

├── credentials/ 

│ └── [DO NOT COMMIT] # GCP service account JSON key (ignored) 

├── .gitignore # Git ignore rules 

└── README.md # 

You're reading it :)


---

## 🔐 Secret Management

⚠️ **IMPORTANT:** Never commit your Google Cloud service account JSON.

Use `.gitignore` to ignore secrets:

```gitignore
# Ignore GCP credentials
credentials/*.json
