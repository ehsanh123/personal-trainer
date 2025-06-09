from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from google.cloud import dialogflowcx_v3 as dialogflow
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions

# === Setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

path_to_key = 'credentials/plenary-stacker-457109-k5-6b664f4fa9ba.json'
api_endpoint_ = 'europe-west2-dialogflow.googleapis.com'
project_id_ = 'plenary-stacker-457109-k5'
location_ = 'europe-west2'
agent_id_ = 'c827abce-ac66-40e5-a7e5-aba7e90b74ae'
session_id_ = 'unique-session-id'

clt1 = None
s_path = None

def set_session():
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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})

@app.post("/chat", response_class=JSONResponse)
async def chat_post(request: Request):
    data = await request.json()
    user_input = data.get("message", "")
    # user_input = 'hey man'
    response_text = await get_response(user_input)
    return {"reply": response_text}

# if __name__ == '__main__':
#     app.run(debug=True)