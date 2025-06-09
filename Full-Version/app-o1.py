from fastapi import FastAPI, Request,UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from google.cloud import dialogflowcx_v3 as dialogflow
#
import os
import json
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions
#
import mediapipe as mp
import cv2
import numpy as np
#
import soundfile as sf
import sounddevice as sd
import io
import speech_recognition as sr
from pydub import AudioSegment
########################### === Setup server === ###########################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


########################### Image upload and processing ###########################
import base64

@app.post("/process-image")
async def process_image(request: Request):
    data = await request.json()
    image_data = data["image"].split(",")[1]  # Remove the data:image/png;base64,
    
    with open("received_image.png", "wb") as f:
        f.write(base64.b64decode(image_data))
    
    # You could now process the image, add filters, resize, etc.
    
    return JSONResponse(content={"message": "Image received and saved."})


##################pose chek

@app.post("/upload-photo")
async def upload_photo(request: Request):
    data = await request.json()
    image_base64 = data["image"].split(",")[1]  # strip the header

    # Decode base64 to image bytes
    img_bytes = base64.b64decode(image_base64)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run MediaPipe Pose detection
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    results = pose.process(image_rgb)

    # Draw pose landmarks on the original image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Encode the modified image to base64 again
    _, buffer = cv2.imencode(".png", image)
    processed_base64 = base64.b64encode(buffer).decode("utf-8")
    data_url = f"data:image/png;base64,{processed_base64}"

    return JSONResponse(content={"processed_image": data_url})

#### Chatbot setup ##############

path_to_key = 'credentials/plenary-stacker-457109-k5-6b664f4fa9ba.json'
# path_to_key = None

api_endpoint_ = 'europe-west2-dialogflow.googleapis.com'
project_id_ = 'plenary-stacker-457109-k5'
location_ = 'europe-west2'
agent_id_ = 'c827abce-ac66-40e5-a7e5-aba7e90b74ae'
session_id_ = 'unique-session-id'

clt1 = None
s_path = None

######

def set_session():
    if path_to_key is None:
        credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS_JSON"))
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        client1 = dialogflow.SessionsClient(
            credentials=credentials,
            client_options=ClientOptions(api_endpoint=api_endpoint_)
        )
    else:
        client1 = dialogflow.SessionsClient(
            credentials=service_account.Credentials.from_service_account_file(path_to_key),
            client_options=ClientOptions(api_endpoint=api_endpoint_)
        )
    
    session_path1 = client1.session_path(project_id_, location_, agent_id_, session_id_)
    return client1, session_path1

async def get_response(message_):
    global clt1, s_path
    if clt1 is None or s_path is None:
        clt1, s_path = set_session()

    try:
        query_input = dialogflow.QueryInput(
            text=dialogflow.TextInput(text=message_),
            language_code='en'
        )
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: clt1.detect_intent(request={"session": s_path, "query_input": query_input})
        )
        return extract_message(response)
    except Exception as e:
        return f'Error: {e}'

def extract_message(response):
    response_messages = response.query_result.response_messages
    message_text = ''
    for message in response_messages:
        if message.text and hasattr(message.text.text, '__iter__'):
            message_text += ''.join(message.text.text)
    if not message_text:
        message_text = response.query_result.fulfillment_text
    return message_text

#######

@app.post("/chat", response_class=JSONResponse)
async def chat_post(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    # user_input = 'hey man'
    response_text = await get_response(user_input)
    return {"reply": response_text}


#### Audio recording and transcription #########

audio_data = None
recording = False

# Set the default samplerate
sd.default.samplerate = 44100

#############
@app.post("/start-transcribe")
async def transcribe_audio1(request: Request):
        global audio_data
        status_message = ''
        input_text = ''
        
        # Step 1: Save audio data to in-memory buffer
        #frequency need to be done right
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, samplerate=sd.default.samplerate, format='WAV') 
        buffer.seek(0)  # Rewind to the beginning of the buffer

        # Step 2: Use recognizer with in-memory buffer
        recognizer = sr.Recognizer()
        with sr.AudioFile(buffer) as source:
            audio = recognizer.record(source)

        # Step 3: Recognize speech using Speech Recognition            
        try:   
            transcript = recognizer.recognize_google(audio)
            input_text = transcript
            status_message = "Recording Done"
        except sr.UnknownValueError:
            status_message = "Could not understand the audio"
        except sr.RequestError as e:
            status_message = f"Request failed: {e}"


        return {'message': status_message , 'input_text': input_text}

#######
@app.post("/start-recording")
async def start_recording(request: Request):

    global audio_data, recording  
    recording_message = 'a'
    
    
    if not recording:
        recording = True

        recording_message = "Recording voice"

        audio_data = sd.rec(5 * sd.default.samplerate, samplerate=sd.default.samplerate, channels=2, dtype="int16")

    else:
        recording = False

        recording_message = "Recording Done"

        sd.stop()
        sd.wait()

    data = {'message': recording_message , 'input_text': ''} 
    return data #JSONResponse(content=data , status_code=200)

####### new  voice thingy
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    input_text = ""
    status_message = "OK"

    try:
        # Step 1: Read the uploaded file bytes
        uploaded_bytes = await file.read()

        # ✅ Step 2: Save the original uploaded file to disk
        with open("uploaded_original_audio.webm", "wb") as f:
            f.write(uploaded_bytes)

        # Step 3: Convert to WAV using pydub
        # original_audio = AudioSegment.from_file(io.BytesIO(uploaded_bytes))
        # wav_io = io.BytesIO()
        # original_audio.export(wav_io, format="wav")
        # wav_io.seek(0)

        # Step 4: Transcribe using speech_recognition
        # with sr.AudioFile(wav_io) as source:
        #     audio = recognizer.record(source)
        #     input_text = recognizer.recognize_google(audio)

        buffer = io.BytesIO()
        sf.write(buffer, uploaded_bytes, samplerate=sd.default.samplerate, format='WAV') 
        buffer.seek(0)  # Rewind to the beginning of the buffer

        # Step 2: Use recognizer with in-memory buffer
        recognizer = sr.Recognizer()
        with sr.AudioFile(buffer) as source:
            audio = recognizer.record(source)

        # Step 3: Recognize speech using Speech Recognition            
        try:   
            transcript = recognizer.recognize_google(audio)
            input_text = transcript
            status_message = "Recording Done"
        except sr.UnknownValueError:
            status_message = "Could not understand the audio"
        except sr.RequestError as e:
            status_message = f"Request failed: {e}"


    except sr.UnknownValueError:
        status_message = "Could not understand the audio"
    except sr.RequestError as e:
        status_message = f"Request failed: {e}"
    except Exception as e:
        status_message = f"Error: {str(e)}"

    return JSONResponse(content={"message": status_message, "input_text": input_text})

############

@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    status_message = ''
    input_text = ''

    try:
        # Step 1: Read uploaded file
        uploaded_bytes = await file.read()

        

        # Step 2: Save original file for verification
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # raw_filename = f"uploaded_audio_{timestamp}.webm"
        # with open(raw_filename, "wb") as f:
        #     f.write(uploaded_bytes)
        audio = AudioSegment.from_file(io.BytesIO(uploaded_bytes))

        
        
        # wav_filename = f"uploaded_audio_1.wav"
        # audio.export(wav_filename, format="wav")

        # Step 3: Convert to WAV using pydub
        # original_audio = AudioSegment.from_file(io.BytesIO(uploaded_bytes))
        # audio_data1, sample_rate = sf.read(io.BytesIO(uploaded_bytes))  # this gives NumPy array

        # audio_data1, sample_rate = sf.read(wav_filename)


        # sf.write("output_copy.wav", audio_data1, sample_rate)


        # sf.write("output.wav", audio_data1, sample_rate)

        wav_io = io.BytesIO()

        # sf.write(wav_io, audio,samplerate=44100,format='WAV')
        #audio_data1, samplerate=sample_rate, format='WAV') 
        

        audio.export(wav_io, format="wav")
        wav_io.seek(0)


        # Step 4: Transcribe using SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)

        try:
            input_text = recognizer.recognize_google(audio)
            status_message = "Recording Done"
        except sr.UnknownValueError:
            status_message = "Could not understand the audio"
        except sr.RequestError as e:
            status_message = f"Request failed: {e}"

    except Exception as e:
        input_text = f"Unexpected error: {str(e)}"

    return JSONResponse(content={
        "message": status_message,
        "input_text": input_text,
    })

#################
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# if __name__ == '__main__':
#     app.run(debug=True)