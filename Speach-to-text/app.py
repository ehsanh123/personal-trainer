from flask import Flask, render_template, request
import os
from pydub import AudioSegment
import speech_recognition as sr
import io

app = Flask(__name__)

# Folder to save audio files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return 'No file part', 400
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return 'No selected file', 400
    if audio_file:
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_path)
        
        # Convert the audio file to WAV format with the correct sample rate if necessary
        converted_audio_path = convert_audio_to_wav(audio_path)
        
        # Process the audio file with SpeechRecognition to get the transcript
        transcript = transcribe_audio(converted_audio_path)
        return f'File saved at {audio_path}. Transcription: {transcript}', 200

def convert_audio_to_wav(input_path):
    """Convert the input audio file to WAV format with 16kHz sample rate"""
    audio = AudioSegment.from_file(input_path)  # Load the audio file
    audio = audio.set_frame_rate(16000)  # Convert to 16kHz sample rate
    output_path = input_path.replace(".webm", "_converted.wav")  # Modify the output path
    audio.export(output_path, format="wav")  # Save as WAV
    return output_path

def transcribe_audio(audio_path):
    """Transcribes the given audio file using SpeechRecognition."""
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        print("Listening to the audio file...")
        audio = recognizer.record(source)  # Read the entire file

    try:
        print("Recognizing...")
        transcript = recognizer.recognize_google(audio)  # Using Google's Web Speech API
        return transcript
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
        return "Error: Could not understand the audio"
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
