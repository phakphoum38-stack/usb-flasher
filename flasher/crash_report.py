import os, traceback
from datetime import datetime

os.makedirs("logs", exist_ok=True)

def send_crash(e):
    try:
        with open("logs/crash.log", "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now()}]\n")
            f.write(str(e) + "\n")
            f.write(traceback.format_exc() + "\n")
    except:
        pass
