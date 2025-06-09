# 🎯 FastAPI Multimedia AI Assistant

This project is a FastAPI-based web application that combines:

- ✅ Image upload and processing
- ✅ Pose detection using MediaPipe
- ✅ Audio recording and transcription
- ✅ Chatbot communication via Google Dialogflow CX

---

## 📦 Features

### 🖼️ Image Upload
- Accepts base64-encoded images
- Saves them and returns a confirmation message

### 🕺 Pose Detection
- Processes uploaded photos with MediaPipe
- Draws pose landmarks and returns the annotated image as a base64-encoded PNG

### 🎙️ Audio Recording & Transcription
- Records 5 seconds of audio from your device using `sounddevice`
- Transcribes speech using `speech_recognition` (Google backend)
- Supports `.webm`/`.wav` uploads with transcription

### 🤖 Chatbot Integration
- Uses Google Dialogflow CX for natural, intelligent chatbot responses
- Responds to typed input with contextual replies

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **MediaPipe** – Pose detection
- **OpenCV / NumPy** – Image handling
- **SpeechRecognition + PyDub + SoundDevice** – Audio processing
- **Dialogflow CX** – AI chatbot (via Google Cloud)
- **Jinja2** – Templating engine for frontend integration

---

## 🧪 API Endpoints

| Endpoint             | Method | Description                          |
|----------------------|--------|--------------------------------------|
| `/process-image`     | POST   | Upload and save base64 image         |
| `/upload-photo`      | POST   | Perform pose detection on image      |
| `/chat`              | POST   | Get reply from Dialogflow CX         |
| `/start-recording`   | POST   | Start or stop 5-sec audio recording  |
| `/start-transcribe`  | POST   | Transcribe the last recorded audio   |
| `/upload-audio`      | POST   | Transcribe uploaded audio file       |
| `/transcribe-audio`  | POST   | Convert and transcribe audio uploads |
| `/`                  | GET    | Return the main index page           |

---

## 🔑 Setup Instructions

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
