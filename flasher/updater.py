import requests, subprocess, os

API="https://api.github.com/repos/phakphoum38-stack/usb-flasher/releases/latest"

def check_update(v):
    try:
        r=requests.get(API,timeout=5).json()
        if r["tag_name"].replace("v","")!=v:
            return r
    except: pass

def download_update(d):
    for a in d["assets"]:
        if a["name"].endswith(".exe"):
            p="update.exe"
            open(p,"wb").write(requests.get(a["browser_download_url"]).content)
            return p

def run_update(p):
    subprocess.Popen([p])
    os._exit(0)

    print("✅ Update downloaded")
    return True
