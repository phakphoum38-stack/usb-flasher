import subprocess

import platform

# =========================

# ❌ DANGER PATTERNS

# =========================

DANGER_KEYWORDS = [

    "c:",

    "windows",

    "system",

    "disk 0",

    "disk0",

    "boot",

]

# =========================

# 🔍 GET REAL DISK INFO (Windows)

# =========================

def get_disk_info():

    disks = []

    try:

        output = subprocess.check_output(

            "wmic diskdrive get DeviceID,Model,Size,MediaType",

            shell=True

        ).decode()

        for line in output.splitlines()[1:]:

            if line.strip():

                parts = line.split()

                device = parts[0]

                model = " ".join(parts[1:-2])

                size = parts[-2]

                media = parts[-1]

                disks.append({

                    "device": device,

                    "model": model,

                    "size": int(size) if size.isdigit() else 0,

                    "media": media.lower()

                })

    except Exception as e:

        print("Disk info error:", e)

    return disks

# =========================

# 🔍 MATCH DEVICE

# =========================

def find_device_info(device):

    disks = get_disk_info()

    for d in disks:

        if device.lower() in d["device"].lower():

            return d

    return None

# =========================

# ⚠️ HARD BLOCK SYSTEM DISK

# =========================

def block_system_disk(device_info):

    if not device_info:

        raise Exception("❌ Unknown device")

    dev = device_info["device"].lower()

    # block disk 0 (usually system)

    if "physicaldrive0" in dev:

        raise Exception("❌ BLOCKED: system disk (disk 0)")

    # block very large disks (> 1TB)

    if device_info["size"] > 1_000_000_000_000:

        raise Exception("❌ BLOCKED: disk too large (likely internal drive)")

    return True

# =========================

# 🔍 BASIC STRING FILTER

# =========================

def check_device(device: str):

    d = device.lower()

    for bad in DANGER_KEYWORDS:

        if bad in d:

            raise Exception(f"❌ BLOCKED: unsafe keyword -> {device}")

    return True

# =========================

# 🔍 USB VALIDATION (REAL)

# =========================

def is_valid_usb(device: str):

    info = find_device_info(device)

    if not info:

        return False

    # must be removable / USB

    if "usb" not in info["media"]:

        return False

    return True

# =========================

# ⚠️ CONFIRMATION (STRONG)

# =========================

def confirm_device(device: str, info: dict):

    print("\n⚠️ WARNING: FLASH TARGET")

    print(f"➡️ Device : {device}")

    print(f"➡️ Model  : {info.get('model')}")

    print(f"➡️ Size   : {round(info.get('size',0)/(1024**3),2)} GB")

    print("\n⚠️ ALL DATA WILL BE LOST!")

    confirm = input("Type EXACT device name to continue: ")

    if confirm.lower() != device.lower():

        raise Exception("❌ Confirmation mismatch")

    return True

# =========================

# 🧠 FULL SAFETY PIPELINE (PRO)

# =========================

def safety_pipeline(device: str):

    if not device:

        raise Exception("❌ No device selected")

    # 1. basic keyword check

    check_device(device)

    # 2. get real disk info

    info = find_device_info(device)

    if not info:

        raise Exception("❌ Device not found")

    # 3. block system disk

    block_system_disk(info)

    # 4. must be USB

    if not is_valid_usb(device):

        raise Exception("❌ Not a USB device")

    # 5. confirm

    confirm_device(device, info)

    return True
