import requests
import json
import time

SERVER_URL = "https://your-server.com/upload-log"


def upload_log(file_path="crash_report.json"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        payload = {
            "time": time.time(),
            "data": data
        }

        r = requests.post(SERVER_URL, json=payload)

        if r.status_code == 200:
            print("📤 Log uploaded successfully")

    except Exception as e:
        print("❌ Upload failed:", e)
