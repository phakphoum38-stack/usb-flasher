import subprocess

def get_usb_devices():
    out = subprocess.check_output(
        "wmic diskdrive get DeviceID,Model",
        shell=True
    ).decode()

    devices = []
    for line in out.splitlines()[1:]:
        if line.strip():
            parts = line.split()
            path = parts[0]
            model = " ".join(parts[1:])
            if "USB" in model.upper():
                devices.append({"path": path, "model": model})

    return devices
