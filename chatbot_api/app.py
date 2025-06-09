from flask import Flask, render_template, redirect, url_for, request
# import os
import speech_recognition as sr
import soundfile as sf
import sounddevice as sd
import io

########################

audio_data = None
sd.default.samplerate = 44100
recording = False
status_message = "Welcome to the Chatbot"
recording_message = "Start Recording"
input_text= ""

########################
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    global clt1, s_path, status_message, recording_message, input_text
    clt1 , s_path = set_session()
    return render_template('index.html', 
    status = status_message , recording1 = recording_message , 
    input_text = input_text)

###################################

@app.route('/start-recording', methods=['POST'])
def start_recording():
    global audio_data, clt1, s_path
    global recording, status_message , recording_message
    if clt1 is None or s_path is None:
      clt1, s_path = set_session()
    ###########
    if not recording:
        recording = True
        status_message = "Stop Recording"
        recording_message = "Recording..."
        audio_data = sd.rec(5 * sd.default.samplerate, samplerate=sd.default.samplerate, channels=2, dtype="int16")
    else:
        recording = False
        recording_message = "Start Recording..."
        sd.stop()
        sd.wait()
        transcribe_audio1()
  
    if input_text != "" and not recording:
        # status_message = get_response(input_text)
        get_response_async(input_text)
        # get_response_async(input_text, callback=set_status_message)
            
    return redirect(url_for('index'))

def set_status_message(message):
    global status_message
    status_message = message

def transcribe_audio1():
        global audio_data, status_message, input_text
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, samplerate=sd.default.samplerate, format='WAV') 
        #frequency need to be done right
        buffer.seek(0)  # Rewind to the beginning of the buffer

        # Step 2: Use recognizer with in-memory buffer
        recognizer = sr.Recognizer()
        with sr.AudioFile(buffer) as source:
            audio = recognizer.record(source)
        try:   
            transcript = recognizer.recognize_google(audio)
            input_text = transcript
            status_message = "Recording Done"
        except sr.UnknownValueError:
            status_message = "Could not understand the audio"
        except sr.RequestError as e:
            status_message = f"Request failed: {e}"

######################################

from google.cloud import dialogflowcx_v3 as dialogflow
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions

path_to_key = 'plenary-stacker-457109-k5-6b664f4fa9ba.json'
api_endpoint_ = 'europe-west2-dialogflow.googleapis.com'
project_id_ = 'plenary-stacker-457109-k5'
location_ = 'europe-west2'
agent_id_ = 'c827abce-ac66-40e5-a7e5-aba7e90b74ae'  
session_id_ = 'unique-session-id'  

###########################
clt1 = dialogflow.SessionsClient()
s_path = clt1.session_path(
    project_id_,location_, agent_id_
    , session_id_)
#########################################
def set_session(
  path = path_to_key,  api_endpoint1 = api_endpoint_,
  project_id1 = project_id_,  loc1 = location_,
  agent_i = agent_id_,  sesion_id1 = session_id_):

  # Provide the path to your service account key file
  client1 = dialogflow.SessionsClient(
     credentials=service_account.Credentials.
     from_service_account_file(path), 
     client_options=ClientOptions(api_endpoint=api_endpoint1))

  session_path1 = client1.session_path(project_id1, 
  loc1, agent_i, sesion_id1)

  return client1, session_path1

############################################
def get_response(masssage_):
    global clt1, s_path,status_message
    if clt1 is None or s_path is None:
      clt1, s_path = set_session()
      
    client = clt1
    session_path = s_path

    ####################################
    try:
        query_input = dialogflow.QueryInput(
            text= dialogflow.TextInput(text=masssage_),
            language_code='en' 
        )
        # Send the query to the agent and get the response
        response = client.detect_intent(
            request={"session": session_path, "query_input": query_input})
        return extract_masage(response)
    except Exception as e:
        return status_message

#################################################
def extract_masage(response):
  #get the massage from reposane
  response_message = response.query_result.response_messages
  message1 = ''
  # Loop through the response messages and extract the text message
  for message in response_message:
    if message.text:
      if hasattr(message.text.text, '__iter__'):
            # If it's iterable (Repeated), join the elements into a single string
            message1 += ''.join(message.text.text)
      else:
            # If it's already a string, concatenate directly
            message1 += message.text.text
  if message1 == '':
    message1 = response.query_result.fulfillment_text
  return message1

######################################


@app.route('/send-button', methods=['POST'])
def send_button():
    global input_text, status_message,clt1, s_path
    if clt1 is None or s_path is None:
      clt1, s_path = set_session()
      return redirect(url_for('index'))
    # input_text = request.args.get('input_text', '')
    # clt , s_path1 = set_session()

    # query_input = dialogflow.QueryInput(
    #     text= dialogflow.TextInput(text=input_text),
    #     language_code='en' 
    # )
    # # Send the query to the agent and get the response
    # response = clt.detect_intent(
    #     request={"session": s_path1, "query_input": query_input})

    # status_message = extract_masage(response)
    input_text = request.form['user-input']
    
    status_message = get_response(input_text)
    # get_response_async(input_text, callback=set_status_message)
    # get_response('hey man', clt, s_path1)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
