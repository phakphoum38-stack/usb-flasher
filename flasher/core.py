import os
from tqdm import tqdm

def flash_image(image, device):
    total = os.path.getsize(image)
    block_size = 4 * 1024 * 1024

    with open(image, "rb") as img, open(device, "wb") as dev:
        with tqdm(total=total, unit='B', unit_scale=True, desc="Flashing") as pbar:
            while True:
                chunk = img.read(block_size)
                if not chunk:
                    break
                dev.write(chunk)
                pbar.update(len(chunk))
