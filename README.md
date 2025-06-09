# 🏋️‍♂️ AI-Powered Personal Trainer

This project is a complete AI-driven personal training system that integrates **pose detection**, **voice interaction**, **chatbot support**, and **gamified learning tools**. It combines computer vision, speech recognition, and conversational AI to create an engaging and intelligent personal trainer experience.

---

## 🧠 Overview

This repository documents the full journey of building an AI-powered personal trainer. It includes:

- ✅ Full-featured working version
- 🧍 Pose detection API
- 🎙️ Voice-to-text chatbot prototypes
- 🧪 Async server testing
- 🕹️ Two simple fitness-related mini games
- 📚 Clear development steps, tests, and modules

---

## 🗂️ Project Structure
├── Full-version/ # 🔧 Final integrated version of the app
├── api_pose_checker/ # 🧍 Standalone pose detection API
├── async_server-master/ # ⚙️ Async server test setup
├── Simple_game/
│ └── Battle_math/ # 🧠 Math battle mini-game
├── Speach-to-text/ # 🎤 Basic speech-to-text test
├── chatbot_api/ # 🤖 Chatbot API integration
├── voice_chatbot_scync/ # 🔊 Synchronous voice-enabled chatbot
├── chatbot_asycn_test/ # 🔄 Async chatbot test
└── README.md # 📘 This file

---

## 🚀 How to Run

### Clone the repo
```bash
git clone https://github.com/your-username/ai-personal-trainer.git
cd ai-personal-trainer
```
## Install dependencies (recommended per folder)
bash
Copy code
cd Full-version
pip install -r requirements.txt

## Run the final app
bash
Copy code

---

## 💡 Key Features

- 📸 **Pose Estimation** – Real-time feedback using MediaPipe
- 🗣️ **Voice Interaction** – Voice input and transcription
- 🤖 **Dialogflow Chatbot** – AI-powered smart responses
- 🎮 **Fitness Mini-Games** – Interactive learning and fun
- ⚙️ **Async APIs** – Built with FastAPI for performance

---

## 📦 Dependencies

- `FastAPI`
- `OpenCV`
- `MediaPipe`
- `NumPy`
- `SpeechRecognition`
- `PyDub` / `SoundDevice`
- `Dialogflow CX`
- `Jinja2`
- `Uvicorn`

> 💡 **Note:** Each folder may have its own `requirements.txt`.

---

## 📌 Notes

- 🔑 You need a **Google Cloud service account key** for Dialogflow integration.
- 🎙️ Microphone and 📷 camera access are required for full functionality.
- 🧩 Designed with modularity for **easy extension or deployment**.

---

## 🧪 In Progress

- 🔄 Voice chatbot with live interaction
- 🚀 Async optimization
- 🧠 Game expansions
- 🌐 Web frontend integration

---

## 📜 License

This project is for **educational and experimental use**.  
Please handle API keys securely and adhere to all relevant **terms of service**.

---
