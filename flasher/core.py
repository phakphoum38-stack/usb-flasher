def flash_image(image, device):
    print(f"[FLASH] Writing {image} → {device}")

    # simulate real flash engine
    import time

    for i in range(0, 101, 10):
        print(f"Progress: {i}%")
        time.sleep(0.2)

    print("Flash complete")
