import argparse
import os
import sys
import hashlib
from tqdm import tqdm

# =========================
# 🔍 LIST DEVICES
# =========================
def list_devices():
    print("\n📦 Available devices:\n")

    if os.name == "nt":
        os.system("wmic diskdrive get DeviceID,Model,Size")
    else:
        os.system("lsblk -o NAME,SIZE,MODEL,TRAN")

# =========================
# ⚠️ SAFETY CHECK
# =========================
def safety_check(device):
    if os.name == "nt":
        if "PhysicalDrive0" in device:
            print("❌ Refusing to flash system disk!")
            sys.exit(1)
    else:
        if device == "/dev/sda":
            print("❌ Refusing to flash system disk!")
            sys.exit(1)

# =========================
# ❗ CONFIRMATION
# =========================
def confirm():
    print("\n⚠️ WARNING: This will ERASE the target disk completely!")
    ans = input("Type YES to continue: ")
    if ans != "YES":
        print("❌ Cancelled")
        sys.exit(0)

# =========================
# 🔥 FLASH FUNCTION
# =========================
def flash(image, device):
    total = os.path.getsize(image)
    block_size = 4 * 1024 * 1024  # 4MB

    try:
        with open(image, "rb") as img, open(device, "wb") as dev:
            with tqdm(total=total, unit='B', unit_scale=True, desc="🔥 Flashing") as pbar:
                while True:
                    chunk = img.read(block_size)
                    if not chunk:
                        break

                    dev.write(chunk)
                    pbar.update(len(chunk))

        print("\n✅ Flash complete")

    except PermissionError:
        print("\n❌ Permission denied (Run as Administrator / sudo)")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

# =========================
# 🔐 HASH VERIFY
# =========================
def get_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

# =========================
# 🚀 MAIN
# =========================
def main():
    parser = argparse.ArgumentParser(description="USB Flasher (.img only)")
    parser.add_argument("--image", required=True, help="Path to .img file")
    parser.add_argument("--device", required=False, help="Target device")

    args = parser.parse_args()

    # ✅ Check image
    if not args.image.endswith(".img"):
        print("❌ Only .img supported in Phase 2")
        sys.exit(1)

    if not os.path.exists(args.image):
        print("❌ Image file not found")
        sys.exit(1)

    # 🔍 Show devices
    list_devices()

    # 🎯 Select device
    device = args.device
    if not device:
        device = input("\nEnter target device (e.g. /dev/sdb or \\\\.\\PhysicalDrive1): ")

    # ⚠️ Safety + Confirm
    safety_check(device)
    confirm()

    # 🔥 Flash
    flash(args.image, device)

    # 🔍 Verify (image hash)
    print("\n🔍 Calculating image hash...")
    image_hash = get_hash(args.image)
    print(f"SHA256: {image_hash}")

    print("\n🎉 Done!")

if __name__ == "__main__":
    main()
