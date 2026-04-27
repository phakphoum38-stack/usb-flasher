import hashlib
from tqdm import tqdm
import argparse
import os
import sys

def get_size(path):
    return os.path.getsize(path)

def list_devices():
    print("\n📦 Available devices (ตรวจเองก่อนเลือก!):\n")

    if os.name == "nt":
        os.system("wmic diskdrive list brief")
    else:
        os.system("lsblk -o NAME,SIZE,MODEL")

def confirm():
    print("\n⚠️ WARNING: This will ERASE the target disk completely!")
    ans = input("Type YES to continue: ")
    if ans != "YES":
        print("❌ Cancelled")
        sys.exit(0)

def flash(image, device):
    total = get_size(image)
    written = 0
    block_size = 4 * 1024 * 1024  # 4MB

    with open(image, "rb") as img, open(device, "wb") as dev:
        while True:
            chunk = img.read(block_size)
            if not chunk:
                break

            dev.write(chunk)
            written += len(chunk)

            percent = (written / total) * 100
            print(f"\r🔥 Flashing: {percent:.2f}%", end="")

    print("\n✅ Flash complete")

def main():
    parser = argparse.ArgumentParser(description="Simple USB Flasher (.img only)")
    parser.add_argument("--image", required=True, help="Path to .img file")
    parser.add_argument("--device", required=False, help="Target device")

    args = parser.parse_args()

    if not args.image.endswith(".img"):
        print("❌ Only .img supported in Phase 1")
        sys.exit(1)

    if not os.path.exists(args.image):
        print("❌ Image file not found")
        sys.exit(1)

    list_devices()

    device = args.device
    if not device:
        device = input("\nEnter target device (e.g. /dev/sdb or \\\\.\\PhysicalDrive1): ")

    confirm()
    flash(args.image, device)

if __name__ == "__main__":
    main()
