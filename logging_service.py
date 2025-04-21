from fastapi import FastAPI, Request
import hazelcast
import os
import signal
import subprocess
import sys
from contextlib import asynccontextmanager

app = FastAPI()

HAZELCAST_PATH = "/Users/petroprokopets/Downloads/hazelcast-5.5.0/bin/hz"
hz_client = None
hz_process = None
log_map = None

local_logs = {}

def start_node():
    global hz_process
    hz_process = subprocess.Popen([HAZELCAST_PATH, "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Hazelcast node started.")

def stop_node():
    global hz_process
    if hz_process:
        os.kill(hz_process.pid, signal.SIGTERM)
        print("Hazelcast node stopped.")
        hz_process = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global hz_client, log_map
    start_node()
    hz_client = hazelcast.HazelcastClient(cluster_members=[])
    log_map = hz_client.get_map("logs").blocking()
    yield
    stop_node()
    if hz_client:
        hz_client.shutdown()
        print("Hazelcast client shutdown gracefully")
app = FastAPI(lifespan=lifespan)

@app.post("/log")
async def store_log(request: Request):
    body = await request.json()
    log_id, msg = body.get("id"), body.get("msg")
    local_logs[log_id] = msg
    if not log_id or not msg:
        return {"message": "Invalid request format"}
    if log_map.contains_key(log_id):
        return {"message": "Message already logged"}
    log_map.put(log_id, msg)
    print(f"Stored message: {log_id} - {msg}")
    return {"status": "logged", "id": log_id}

@app.get("/log")
def get_logs():
    return local_logs