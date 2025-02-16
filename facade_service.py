from fastapi import FastAPI, Request
import requests
import uuid
import time

app = FastAPI()

LOGGING_SERVICE_URL = "http://127.0.0.1:8001/log"
MESSAGES_SERVICE_URL = "http://127.0.0.1:8002/message"
MAX_RETRIES = 3
RETRY_DELAY = 1

@app.post("/send")
async def send_message(request: Request):
    body = await request.json()
    msg = body.get("msg")
    message_id = str(uuid.uuid4())
    data = {"id": message_id, "msg": msg}
    for _ in range(MAX_RETRIES):
        try:
            requests.post(LOGGING_SERVICE_URL, json=data)
            return {"message": "Message sent"}
        except:
            print("One more try")
            time.sleep(RETRY_DELAY)
    return { "message": "Logging service unreachable"}

@app.get("/fetch")
def fetch_messages():
    try:
        logs = requests.get(LOGGING_SERVICE_URL).json()
        static_message = requests.get(MESSAGES_SERVICE_URL).json()
        return {"logs": logs, "message": static_message}
    except:
        return { "message": "Something went wrong" }
