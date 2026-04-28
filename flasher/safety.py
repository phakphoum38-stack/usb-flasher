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
    "ssd",
    "boot"
]

# =========================
# 🔍 BASIC SAFETY CHECK
# =========================
def check_device(device: str):
    d = device.lower()

    for bad in DANGER_KEYWORDS:
        if bad in d:
            raise Exception(f"❌ BLOCKED: unsafe device detected -> {device}")

    return True


# =========================
# ⚠️ CONFIRMATION LAYER
# =========================
def confirm_device(device: str):
    print("\n⚠️ WARNING: You are about to FLASH this device:")
    print("➡️", device)
    print("⚠️ ALL DATA WILL BE LOST!")

    confirm = input("Type YES to continue: ")

    if confirm != "YES":
        raise Exception("❌ Cancelled by user")

    return True


# =========================
# 🔍 USB VALIDATION (basic cross-platform)
# =========================
def is_valid_usb(device: str):
    """
    simple heuristic check
    (real tool would use disk enumeration)
    """

    if device is None:
        return False

    d = device.lower()

    # block system disks
    if any(x in d for x in ["system", "windows", "macintosh", "linux"]):
        return False

    return True


# =========================
# 🧠 FULL SAFETY PIPELINE
# =========================
def safety_pipeline(device: str):
    """
    Use this in GUI instead of check_device directly
    """

    if not is_valid_usb(device):
        raise Exception("❌ Not a valid USB device")

    check_device(device)
    confirm_device(device)

    return True
