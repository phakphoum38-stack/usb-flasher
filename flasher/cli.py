import argparse
from flasher.core import flash_image
from flasher.devices import get_usb_devices
from flasher.verify import verify_flash
from flasher.iso import convert_iso_to_img

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)

    args = parser.parse_args()
    image = args.image

    if image.endswith(".iso"):
        print("📀 Converting ISO → IMG...")
        image = convert_iso_to_img(image)

    devices = get_usb_devices()

    print("\nSelect device:")
    for i, d in enumerate(devices):
        print(f"[{i}] {d}")

    choice = int(input("Choose: "))
    device = devices[choice]

    confirm = input("Type YES: ")
    if confirm != "YES":
        return

    flash_image(image, device)
    verify_flash(image, device)
