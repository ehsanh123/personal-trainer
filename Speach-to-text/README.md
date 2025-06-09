# Audio Transcription Web App

## Overview
This Flask-based web application allows users to upload audio files (e.g., `.webm`), which are then converted into a `.wav` format, transcribed using Google's Web Speech API, and returned with the transcript. The app uses the `pydub` library to handle audio conversion and the `speech_recognition` library to perform speech-to-text functionality.

## Features
- Upload an audio file for transcription.
- Automatically converts non-WAV audio files to WAV format with a 16kHz sample rate.
- Transcribes the audio using Google's Web Speech API.
- Displays the transcribed text on the web page.

## Prerequisites
- Python 3.x
- Required Python libraries: Flask, pydub, speech_recognition
- you might need to download ffmpeg and add it to envorimental varibles of your system

### Install dependencies:
```bash
pip install Flask pydub SpeechRecognition
