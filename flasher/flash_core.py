import os
import platform
import subprocess
from flasher.utils import resource_path


# =========================
# 🔍 LIST DISKS
# =========================
def list_disks():
    sys = platform.system()

    if sys == "Windows":
        return list_disks_windows()
    elif sys == "Linux":
        return list_disks_linux()
    elif sys == "Darwin":
        return list_disks_macos()
    else:
        raise Exception("Unsupported OS")


def list_disks_windows():
    out = subprocess.check_output("wmic diskdrive get name,size,model", shell=True).decode()
    return out


def list_disks_linux():
    out = subprocess.check_output("lsblk -o NAME,SIZE,MODEL", shell=True).decode()
    return out


def list_disks_macos():
    out = subprocess.check_output("diskutil list", shell=True).decode()
    return out
