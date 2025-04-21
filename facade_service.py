from fastapi import FastAPI, Request
import requests
import uuid
import time
import random
import hazelcast

app = FastAPI()

LOGGING_SERVICE_INSTANCES = ["http://127.0.0.1:8001","http://127.0.0.1:8002","http://127.0.0.1:8003"]
MESSAGES_SERVICE_INSTANCES = ["http://127.0.0.1:8004", "http://127.0.0.1:8005"]

MAX_RETRIES = 3
RETRY_DELAY = 1

hz_client = hazelcast.HazelcastClient(cluster_members=[])
message_queue = hz_client.get_queue("messages").blocking()

def get_random_logging_service():
    return random.choice(LOGGING_SERVICE_INSTANCES)

def get_random_messages_service():
    return random.choice(MESSAGES_SERVICE_INSTANCES)

@app.post("/send")
async def send_message(request: Request):
    body = await request.json()
    msg = body.get("msg")
    message_id = str(uuid.uuid4())
    data = {"id": message_id, "msg": msg}
    logging_service_url = get_random_logging_service() + "/log"
    for _ in range(MAX_RETRIES):
        print(logging_service_url," sends", data)
        try:
            response = requests.post(logging_service_url, json=data)
            message_queue.offer(data)
            print(f"Message added to queue: {data}")
            return {"message": "Message sent", "logging_service": logging_service_url, "response": response.json()}
        except:
            print("Retrying...")
            time.sleep(RETRY_DELAY)

    return {"message": "Logging service unreachable"}

@app.get("/fetch")
def fetch_messages():
    logs = {}
    for service_url in LOGGING_SERVICE_INSTANCES:
        try:
            logs[service_url] = requests.get(f"{service_url}/log").json()
        except requests.exceptions.RequestException as e:
            logs[service_url] = {"message": str(e)}
    messages_service_url = get_random_messages_service()
    try:
        messages = requests.get(f"{messages_service_url}/message").json()
    except requests.exceptions.RequestException as e:
        messages = {"error": str(e)}
    
    return {
        "logs": logs,
        "messages": messages,
        "messages_service": messages_service_url
    }

@app.on_event("shutdown")
def shutdown_event():
    hz_client.shutdown()
    print("Hazelcast client shutdown gracefully")