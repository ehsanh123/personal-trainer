from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Folder to save audio files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('save_audio.html')

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
        return f'File saved at {audio_path}', 200

if __name__ == '__main__':
    app.run(debug=True)
