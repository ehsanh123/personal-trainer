🤖 Chatbot with FastAPI & Dialogflow CX
This is a simple chatbot web app using FastAPI + Dialogflow CX. The user sends a message via the browser, and the backend fetches a response from your Dialogflow agent.

🚀 Setup
Install dependencies:

bash
pip install fastapi uvicorn google-cloud-dialogflow-cx jinja2 soundfile sounddevice
Create folders:

bash

mkdir templates static
Add your HTML UI to templates/index2.html.

Place your Dialogflow CX key in the project and set path_to_key in app2.py.

Run the app:

bash
uvicorn app2:app --reload
