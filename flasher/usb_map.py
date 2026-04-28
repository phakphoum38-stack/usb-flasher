import platform
import subprocess
import re

# =========================
# 🔍 REAL DEVICE PARSER
# =========================
def get_real_usb_devices():
    sys = platform.system()
    devices = []

    if sys == "Windows":
        out = subprocess.check_output(
            "wmic diskdrive get DeviceID,Model,Size,InterfaceType",
            shell=True
        ).decode(errors="ignore")

        for line in out.split("\n"):
            if "USB" in line or "GB" in line:
                devices.append(parse_windows(line))

    elif sys == "Linux":
        out = subprocess.check_output(
            "lsblk -o NAME,SIZE,MODEL,TRAN",
            shell=True
        ).decode()

        for line in out.split("\n"):
            if "usb" in line.lower():
                devices.append({"raw": line})

    return devices


# =========================
# 🧠 PARSER (Windows)
# =========================
def parse_windows(line):
    size_match = re.search(r"\d+", line)
    return {
        "raw": line,
        "size": size_match.group() if size_match else "0"
    }
