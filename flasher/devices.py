import subprocess

def get_usb_devices():
    devices = []

    try:
        output = subprocess.check_output("wmic diskdrive get DeviceID,Model,Size", shell=True).decode()

        for line in output.splitlines()[1:]:
            if line.strip():
                parts = line.split()
                path = parts[0]
                model = " ".join(parts[1:-1])
                size = parts[-1]

                # filter removable (ง่าย ๆ)
                if "USB" in model.upper():
                    devices.append({
                        "path": path,
                        "model": model,
                        "size": size
                    })

    except Exception as e:
        print("Device error:", e)

    return devices
