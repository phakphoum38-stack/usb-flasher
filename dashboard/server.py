from fastapi import FastAPI, Request
import json
import time

app = FastAPI()

LOG_FILE = "logs.json"


@app.post("/log")
async def log(request: Request):
    data = await request.json()

    entry = {
        "time": time.time(),
        "data": data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return {"status": "ok"}
