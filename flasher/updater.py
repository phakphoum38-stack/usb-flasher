import requests
import os
import shutil

CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://your-server.com/version.json"


def check_update():
    try:
        data = requests.get(UPDATE_URL).json()

        latest = data["version"]
        url = data["url"]

        if latest != CURRENT_VERSION:
            return download_update(url)

        return False

    except Exception as e:
        print("Update check failed:", e)
        return False


def download_update(url):
    print("⬇️ Downloading update...")

    r = requests.get(url, stream=True)

    with open("update.zip", "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

    print("✅ Update downloaded")
    return True
