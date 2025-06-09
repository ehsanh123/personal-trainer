from flask import Flask, render_template, redirect, url_for, request
# import os
import speech_recognition as sr
import soundfile as sf
import sounddevice as sd
import io
###########
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
########################

# audio_data = None
# sd.default.samplerate = 44100
# recording = False
# status_message = "Welcome to the Chatbot"
# recording_message = "Start Recording"
# input_text= ""

########################
templates = Jinja2Templates(directory="templates")

app = FastAPI()#Flask(__name__)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):  
    global clt1, s_path
    clt1 , s_path = set_session()
    return templates.TemplateResponse("index2.html", {"request": request,
            'res1': 'Welcome to the Chatbot'})

    # return render_template('index.html', 
    # status = status_message , recording1 = recording_message , 
    # input_text = input_text)

###################################

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

clt1 = dialogflow.SessionsClient()
s_path = clt1.session_path(
    project_id_,location_, agent_id_
    , session_id_)

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
    global clt1, s_path
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
        return 'Error: {}'.format(e)
    

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

##############################

@app.post('/chat')
async  def send_button(request: Request):
    

    global clt1, s_path
    if clt1 is None or s_path is None:
        clt1, s_path = set_session()
        return templates.TemplateResponse("index2.html", 
        {"request": request, 'res1': 'setting up, try again'})
    
    data = await request.json()
    
    message = data.get("message")

    query_input = dialogflow.QueryInput(
            text= dialogflow.TextInput(text=message),
            language_code='en' 
        )
    
    # return templates.TemplateResponse("index2.html", 
    #     {"request": request, 'res1': 'hi'})
    #####################
    try:
        response = clt1.detect_intent(
            request={"session": s_path, "query_input": query_input})
        r1 =  extract_masage(response)
        # response = await  clt1.detect_intent(
            # request={"session": s_path, "query_input": query_input})
    
        # r1 = extract_masage(response)
    # print(r1)
        return templates.TemplateResponse("index2.html", 
        {"request": request, 'res1': r1})
    
    except Exception as e:
        return templates.TemplateResponse("index2.html", 
        {"request": request, 'res1': 'Error: {}'.format(e)})
    # return JSONResponse(content={"response": r1})


if __name__ == '__main__':
    app.run(debug=True)
