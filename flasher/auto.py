from flasher.formats import prepare_image
from flasher.devices import get_usb_devices
from flasher.core import flash_image
from flasher.verify import verify_flash
from flasher.efi import generate_config

def auto_build(image):
    print("🚀 AUTO BUILD START")

    img = prepare_image(image)

    devices = get_usb_devices()
    for i, d in enumerate(devices):
        print(f"[{i}] {d['path']}")

    choice = int(input("Select device: "))
    device = devices[choice]["path"]

    print("⚙️ Generating EFI...")
    generate_config("build")

    print("🔥 Flashing...")
    flash_image(img, device)

    print("🔍 Verifying...")
    verify_flash(img, device)

    print("🎉 DONE")
