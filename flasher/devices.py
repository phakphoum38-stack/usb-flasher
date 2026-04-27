import os

def get_usb_devices():
    devices = []

    if os.name == "nt":
        output = os.popen("wmic diskdrive get DeviceID,Model,Size").read()
        lines = output.split("\n")[1:]

        for line in lines:
            if "USB" in line.upper():
                devices.append(line.strip())
    else:
        output = os.popen("lsblk -o NAME,SIZE,TRAN").read()
        for line in output.split("\n"):
            if "usb" in line:
                devices.append("/dev/" + line.split()[0])

    return devices
