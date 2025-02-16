from fastapi import FastAPI, Request

app = FastAPI()
logs = {}

@app.post("/log")
async def store_log(request: Request):
    body = await request.json()
    log_id = body.get("id")
    msg = body.get("msg")
    if not log_id or not msg:
        return {"message": "Invalid request format"}
    logs[log_id] = msg
    return {"status": "logged", "id": log_id}

@app.get("/log")
def get_logs():
    return list(logs.values())
