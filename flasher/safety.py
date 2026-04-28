def safety_pipeline(device: str):
    if not device:
        raise Exception("No device selected")

    d = device.lower()

    if "physicaldrive0" in d:
        raise Exception("BLOCKED: system disk")

    return True
