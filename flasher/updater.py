import requests, subprocess, os

API = "https://api.github.com/repos/phakphoum38-stack/usb-flasher/releases/latest"

def parse(v):
    return tuple(map(int, v.split(".")))

def check_update(current):
    try:
        r = requests.get(API, timeout=5).json()
        latest = r["tag_name"].replace("v", "")

        if parse(latest) > parse(current):
            return r
    except:
        return None

def download_update(d):
    for a in d["assets"]:
        if a["name"].endswith(".exe"):
            path = "update.exe"
            open(path, "wb").write(requests.get(a["browser_download_url"]).content)
            return path

def run_update(p):
    subprocess.Popen([p])
    os._exit(0)
