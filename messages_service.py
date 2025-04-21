from fastapi import FastAPI
import hazelcast
import threading
import time
import sys

app = FastAPI()

stored_messages = {}
hz_client = hazelcast.HazelcastClient(cluster_members=[])
message_queue = hz_client.get_queue("messages").blocking()
def message_consumer():
    print("Message consumer started")
    while True:
        try:
            message = message_queue.poll(timeout=5)
            if message:
                message_id = message["id"]
                msg = message["msg"]
                print(f"Received message: {message_id} - {msg}")
                stored_messages[message_id] = msg
        except Exception as e:
            print(f"Error in consumer: {e}")
            time.sleep(1)
consumer_thread = threading.Thread(target=message_consumer, daemon=True)
consumer_thread.start()

@app.get("/message")
def get_message():
    return stored_messages

@app.on_event("shutdown")
def shutdown_event():
    hz_client.shutdown()
    print("Hazelcast client shutdown gracefully")
