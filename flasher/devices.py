import subprocess

def get_usb_devices():
    devices = []

    try:
        cmd = 'powershell "Get-Disk | Select Number,FriendlyName,BusType"'
        out = subprocess.check_output(cmd, shell=True).decode(errors="ignore")

        for line in out.splitlines()[2:]:
            if "USB" in line.upper():
                parts = line.split()
                if len(parts) >= 2:
                    num = parts[0]
                    model = " ".join(parts[1:])
                    devices.append({
                        "path": f"\\\\.\\PhysicalDrive{num}",
                        "model": model
                    })

    except Exception as e:
        print("Device error:", e)

    return devices
