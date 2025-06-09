# 🧠 Async Data Downloader with Flask + JavaScript

This is a simple web app that simulates downloading data from a remote service. It uses **Flask** for the backend and **JavaScript** to handle async UI updates like in classic ASP.NET Web Forms.

## 🚀 Features

- Button-based trigger to simulate a service call
- Step-by-step status updates:
  - "Connecting to service..."
  - "Getting data..."
  - "Operation complete."
- Result displayed dynamically without page reload
- Fully async flow using JavaScript + Fetch API

---

## 📁 Project Structure

Test_async/ 
├── app.py # Flask backend logic 
├── templates/ 
│ └── index.html # HTML page using Jinja2 templating 
├── static/ 
│ └── script.js # JavaScript for async fetch and status updates 
├── README.md # Project description and usage guide 
└── requirements.txt # Python dependencies

---

## ⚙️ Installation & Running Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/test-async-flask.git
cd test-async-flask
