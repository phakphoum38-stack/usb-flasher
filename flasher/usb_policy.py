import platform
import subprocess

# =========================
# 🧠 CONFIG (ปรับได้)
# =========================
ALLOWED_VENDOR_KEYWORDS = [
    "sandisk",
    "kingston",
    "samsung",
    "lexar",
    "generic"
]

MIN_SIZE_GB = 4


# =========================
# 🔍 GET USB LIST
# =========================
def get_usb_devices():
    sys = platform.system()

    devices = []

    if sys == "Windows":
        out = subprocess.check_output("wmic diskdrive get model,size", shell=True).decode()

        for line in out.split("\n"):
            if "GB" in line or "MB" in line:
                devices.append({"raw": line})

    elif sys == "Linux":
        out = subprocess.check_output("lsblk -o NAME,SIZE,MODEL", shell=True).decode()
        for line in out.split("\n"):
            if line.strip():
                devices.append({"raw": line})

    else:
        out = subprocess.check_output("diskutil list", shell=True).decode()
        devices.append({"raw": out})

    return devices


# =========================
# 🛑 WHITELIST CHECK
# =========================
def is_allowed_device(device_str: str):
    d = device_str.lower()

    return any(v in d for v in ALLOWED_VENDOR_KEYWORDS)


# =========================
# 🔒 SAFE SELECT FILTER
# =========================
def filter_safe_devices(devices):
    safe = []

    for d in devices:
        if is_allowed_device(d["raw"]):
            safe.append(d)

    return safe
