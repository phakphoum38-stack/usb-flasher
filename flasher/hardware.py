import platform
import subprocess

def get_hw():
    hw = {
        "cpu": "",
        "gpu": "",
        "type": "desktop"
    }

    try:
        if platform.system() == "Windows":
            cpu = subprocess.check_output("wmic cpu get name", shell=True).decode()
            gpu = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode()

            hw["cpu"] = cpu.split("\n")[1].strip()
            hw["gpu"] = gpu.split("\n")[1].strip()

    except:
        pass

    if "mobile" in hw["cpu"].lower():
        hw["type"] = "laptop"

    return hw
