import os
import traceback
import json
from datetime import datetime

# 👉 ถ้ามี server ค่อยใส่ URL
CRASH_SERVER = None  # เช่น "https://your-server.com/crash"

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def send_crash(e):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        crash_data = {
            "time": timestamp,
            "error": str(e),
            "trace": traceback.format_exc()
        }

        # =========================
        # 💾 SAVE LOCAL LOG
        # =========================
        with open(os.path.join(LOG_DIR, "crash.log"), "a", encoding="utf-8") as f:
            f.write(json.dumps(crash_data, ensure_ascii=False) + "\n")

        # =========================
        # 🌐 SEND TO SERVER (optional)
        # =========================
        if CRASH_SERVER:
            try:
                import requests
                requests.post(CRASH_SERVER, json=crash_data, timeout=3)
            except:
                pass

        # =========================
        # 🖥️ DEBUG OUTPUT
        # =========================
        print("CRASH:", crash_data["error"])
        print(crash_data["trace"])

    except Exception as err:
        print("Crash handler failed:", err)
