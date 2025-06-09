#########
path_to_key = 'credentials/plenary-stacker-457109-k5-6b664f4fa9ba.json'
# path_to_key = None
############

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
import math

#
import soundfile as sf
import sounddevice as sd
import io
import speech_recognition as sr
from pydub import AudioSegment
import base64
########################### === Setup server === ###########################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
################angle detection and pose detection##################
ref_1_angle = None
ref_2_angle = None
#####################
def calculate_angle(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Calculate vectors
    vector1 = (x1 - x2, y1 - y2)
    vector2 = (x3 - x2, y3 - y2)

    # Calculate dot product
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    # Calculate magnitudes (lengths) of the vectors
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

    # Calculate cosine of the angle
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0  # Handle cases where points are the same
    cos_theta = dot_product / (magnitude1 * magnitude2)

    # Ensure cos_theta is within the valid range [-1, 1] due to potential floating-point errors
    cos_theta = max(-1.0, min(1.0, cos_theta))

    # Calculate the angle in radians and convert to degrees
    angle_radians = math.acos(cos_theta)
    angle_degrees = math.degrees(angle_radians)

    angle_degrees = angle_degrees-angle_degrees%1
    return angle_degrees

# Function to extract the coordinates of a landmark
def get_landmark_coordinates(landmarks, landmark_id):
    try:
        x = landmarks.landmark[landmark_id].x
        y = landmarks.landmark[landmark_id].y
        x=x/1
        y=y/1
        return np.array([x, y])
    except:
        return np.array([0, 0])  # Return [0, 0] if landmark is not detected

def calculate_angles_landmarks(landmarks, mp_pose):
        # Left side angles
        left_shoulder = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        left_elbow = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
        left_wrist = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
        #
        right_shoulder = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        right_elbow = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW)
        right_wrist = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
        #
        left_hip = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        left_knee = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        #
        right_hip = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
        right_knee = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
        #
        left_ankle = get_landmark_coordinates(landmarks,mp_pose.PoseLandmark.LEFT_ANKLE)
        right_ankle = get_landmark_coordinates(landmarks,mp_pose.PoseLandmark.RIGHT_ANKLE)
        #

        if np.any(left_shoulder) and np.any(left_elbow) and np.any(left_wrist):
            left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        else: left_elbow_angle = 0

        if np.any(left_shoulder) and np.any(left_hip) and np.any(left_knee):
            left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
        else:  left_hip_angle = 0

        if np.any(right_shoulder) and np.any(right_elbow) and np.any(right_wrist):
            right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        else:   right_elbow_angle = 0

        if np.any(right_shoulder) and np.any(right_hip) and np.any(right_knee):
            right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
        else:  right_hip_angle = 0

        if np.any(right_knee) and np.any(right_ankle) and np.any(right_hip):
            right_knee_angle = calculate_angle(right_knee, right_ankle, right_hip)
        else:   right_knee_angle = 0

        if np.any(left_knee) and np.any(left_ankle) and np.any(left_hip):
            left_knee_angle = calculate_angle(left_knee, left_ankle, left_hip)
        else:  left_knee_angle = 0


        # Additional angles (e.g., shoulders, knees, etc.)
        head0 = 0
        num = 0
        head = get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.NOSE)
        if not np.array_equal(head, head0): num += 1
        head0 = head

        head += get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_EYE)
        if (head[0]==head0[0]) & (head[1]==head0[1]): num += 1
        head0 = head

        head += get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_EYE)
        if (head[0]==head0[0]) & (head[1]==head0[1]): num += 1
        head0 = head

        head += get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.RIGHT_EAR)
        if (head[0]==head0[0]) & (head[1]==head0[1]): num += 1
        head0 = head

        head += get_landmark_coordinates(landmarks, mp_pose.PoseLandmark.LEFT_EAR)
        if (head[0]==head0[0]) & (head[1]==head0[1]): num += 1
        head0 = head

        head /= num

        if np.any(head) and np.any(left_shoulder) and np.any(left_elbow):
            left_arm_angle = calculate_angle(head, left_shoulder, left_elbow)
        else:
            left_arm_angle = 0

        if np.any(head) and np.any(right_shoulder) and np.any(right_elbow):
            right_arm_angle = calculate_angle(head, right_shoulder, right_elbow)
        else:
            right_arm_angle = 0

        if np.any(head) and np.any(left_shoulder) and np.any(left_hip):
            left_back_angle = calculate_angle(head, left_shoulder, left_hip)
        else:
            left_back_angle = 0

        if np.any(head) and np.any(right_shoulder) and np.any(right_hip):
            right_back_angle = calculate_angle(head, right_shoulder, right_hip)
        else:
            right_back_angle = 0
        ###############
        angles = {
                "left_elbow_angle": left_elbow_angle,
                "left_hip_angle": left_hip_angle,
                "right_elbow_angle": right_elbow_angle,
                "right_hip_angle": right_hip_angle,
                "left_arm_angle": left_arm_angle,
                "right_arm_angle": right_arm_angle,
                "left_back_angle": left_back_angle,
                "right_back_angle": right_back_angle,
                "left_knee_angle": left_knee_angle,
                "right_knee_angle": right_knee_angle
        }

        locations={
            "left_shoulder":left_shoulder,
            "left_elbow":left_elbow,
            "left_wrist":left_wrist,
            "right_shoulder":right_shoulder,
            "right_elbow":right_elbow,
            "right_wrist":right_wrist,

            "head":head,

            "left_hip":left_hip,
            "left_knee":left_knee,
            "left_ankle":left_ankle,

            "right_hip":right_hip,
            "right_knee":right_knee,
            "right_ankle":right_ankle
        }
        return angles,locations


# Function to calculate the angles for both left and right sides and overlay on image
def calculate_and_display_angles(image1, return_angles=False):
    
        
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5,
        static_image_mode=False, model_complexity=0,
        enable_segmentation=False)

    if return_angles == False:
        pose = mp_pose.Pose(
            static_image_mode=True, model_complexity=2,
            enable_segmentation=False, min_detection_confidence=0.1, 
            min_tracking_confidence=0.5)
        
    image = image1.copy()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get pose landmarks
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        ang , locs = calculate_angles_landmarks(results.pose_landmarks , mp_pose)
        if return_angles:
            return ang
        
        # Draw selected points manually
        locations = (
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_ELBOW,
            mp_pose.PoseLandmark.RIGHT_WRIST,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE,
            mp_pose.PoseLandmark.RIGHT_HIP,
            mp_pose.PoseLandmark.RIGHT_KNEE,
            mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.RIGHT_ANKLE
        )


        for loc in locations:
            landmark = results.pose_landmarks.landmark[loc]
            h, w, _ = image.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(image, (cx, cy), 3, (0, 0, 255), cv2.FILLED)

        # # Draw the pose landmarks on the image
        # mp.solutions.drawing_utils
        
        # mp_drawing = mp.solutions.drawing_utils
        # mp_drawing.draw_landmarks(image, locations, mp_pose.POSE_CONNECTIONS)
        
        # Display the angle values at corresponding locations
        def overlay_angle(angle, location, color=(0, 255, 0)):
            # Coordinates are normalized, scale them to the image size
            x = int(location[0] * image.shape[1])
            y = int(location[1] * image.shape[0])
            
            cv2.putText(image, f'{angle:.0f}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

        # Overlay angles on the image
        if np.any(ang['left_elbow_angle']!=0):
            overlay_angle(ang['left_elbow_angle'], locs['left_elbow'], (0, 255, 0))  # Left elbow angle
        if np.any(ang['right_elbow_angle']!=0):
            overlay_angle(ang['right_elbow_angle'], locs['right_elbow'], (0, 255, 0))  # Right elbow angle
        if np.any(ang['left_hip_angle']!=0):
            overlay_angle(ang['left_hip_angle'], locs['left_hip'], (0, 255, 0))  # Left hip angle
        if np.any(ang['right_hip_angle']!=0):
            overlay_angle(ang['right_hip_angle'], locs['right_hip'], (0, 255, 0))  # Right hip angle
        if np.any(ang['left_arm_angle']!=0):
            overlay_angle(ang['left_arm_angle'], (locs['left_shoulder']
                                                   + locs['left_elbow'])/2, (0, 255, 0))  # Left arm angle
        if np.any(ang['right_arm_angle']!=0):
            overlay_angle(ang['right_arm_angle'], (locs['right_shoulder']
                                                   + locs['right_elbow'])/2, (0, 255, 0))
        if np.any(ang['left_back_angle']!=0):
            overlay_angle(ang['left_back_angle'], locs['left_shoulder'], (0, 255, 0))  # Left back angle
        if np.any(ang['right_back_angle']!=0):
            overlay_angle(ang['right_back_angle'], locs['right_shoulder'], (0, 255, 0))  # Right back angle

        if np.any(ang['left_knee_angle']!=0):
            overlay_angle(ang['left_knee_angle'], locs['left_knee'], (0, 255, 0))  # Left knee angle

        if np.any(ang['right_knee_angle']!=0):
            overlay_angle(ang['right_knee_angle'], locs['right_knee'], (0, 255, 0))  # Right knee angle

        return image ,ang
    else:
        return image , None

##################pose chek

@app.post("/upload-photo")
async def Pose_detector(request: Request):
    data = await request.json()
    image_base64 = data["image"].split(",")[1]  # strip the header
    ref_name = data["name"]

    # Decode base64 to image bytes
    img_bytes = base64.b64decode(image_base64)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    image2, ang = None , None#calculate_and_display_angles(image, return_angles=False)

    #caculate and copmare angles
    if ref_name == '1' or ref_name == '2':
        image2, ang = calculate_and_display_angles(image, return_angles=False)    
    global ref_1_angle, ref_2_angle
    if ref_name == '1':
        ref_1_angle = ang
    elif ref_name == '2':
        ref_2_angle = ang
    else:
        ang = calculate_and_display_angles(image, return_angles=True)
        
        if ref_1_angle is not None and ref_2_angle is not None:
            ang_diff = {key: abs(ref_1_angle[key] - ref_2_angle[key]) for key in ref_1_angle.keys()}
            ang = ang_diff
        
        return JSONResponse(content={"processed_image": None , "angles": ang})
    
    
    _, buffer = cv2.imencode(".png", image2)
    processed_base64 = base64.b64encode(buffer).decode("utf-8")
    data_url = f"data:image/png;base64,{processed_base64}"

    return JSONResponse(content={"processed_image": data_url, "angles": ang})

#### Audio recording and transcription #########

@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    status_message = ''
    input_text = ''

    try:
        # Step 1: Read uploaded file
        uploaded_bytes = await file.read()
        # Step 2: Save the audio file in buffer
        audio = AudioSegment.from_file(io.BytesIO(uploaded_bytes))
        wav_io = io.BytesIO()
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
        input_text = "Error "
        status_message = f"Unexpected error: {str(e)}"

    return JSONResponse(content={
        "message": status_message,
        "input_text": input_text,
    })

########## Chatbot setup ##############



clt1 = None
s_path = None

def set_session():
    api_endpoint_ = 'europe-west2-dialogflow.googleapis.com'
    project_id_ = 'plenary-stacker-457109-k5'
    session_id_ = 'unique-session-id'
    location_ = 'europe-west2'
    agent_id_ = 'c827abce-ac66-40e5-a7e5-aba7e90b74ae'

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

####### Chatbot API ###########

@app.post("/chat", response_class=JSONResponse)
async def chat_post(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    # user_input = 'hey man'
    response_text = await get_response(user_input)
    return {"reply": response_text}

###########basic API for testing ###########`
# `
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
