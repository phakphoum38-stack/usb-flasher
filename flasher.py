import argparse
import os
import sys
import hashlib
import re
from tqdm import tqdm

# =========================
# 🔍 GET USB DEVICES
# =========================
def get_usb_devices():
    devices = []

    if os.name == "nt":
        # Windows
        output = os.popen("wmic diskdrive get DeviceID,Model,Size").read()
        lines = output.strip().split("\n")[1:]

        for line in lines:
            if line.strip():
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 3:
                    device_id = parts[0]
                    model = parts[1]
                    size = parts[2]

                    # กัน system disk
                    if "0" in device_id:
                        continue

                    devices.append({
                        "path": device_id,
                        "model": model,
                        "size": size
                    })

    else:
        # Linux
        output = os.popen("lsblk -o NAME,SIZE,MODEL,TRAN").read()
        lines = output.strip().split("\n")[1:]

        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                name, size, model, tran = parts[0], parts[1], parts[2], parts[3]

                if tran == "usb":
                    devices.append({
                        "path": f"/dev/{name}",
                        "model": model,
                        "size": size
                    })

    return devices

# =========================
# 📦 SHOW & SELECT DEVICE
# =========================
def select_device():
    devices = get_usb_devices()

    if not devices:
        print("❌ No USB devices found")
        sys.exit(1)

    print("\n📦 Select USB device:\n")

    for i, d in enumerate(devices):
        print(f"[{i}] {d['path']} | {d['model']} | {d['size']}")

    while True:
        choice = input("\nEnter number: ")
        if choice.isdigit() and int(choice) < len(devices):
            return devices[int(choice)]["path"]
        else:
            print("❌ Invalid selection")

# =========================
# ⚠️ CONFIRM
# =========================
def confirm(device):
    print(f"\n⚠️ This will ERASE: {device}")
    ans = input("Type YES to continue: ")
    if ans != "YES":
        print("❌ Cancelled")
        sys.exit(0)

# =========================
# 🔥 FLASH
# =========================
def flash(image, device):
    total = os.path.getsize(image)
    block_size = 4 * 1024 * 1024

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
        print("\n❌ Run as Administrator / sudo")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

# =========================
# 🔐 HASH
# =========================
def get_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

# =========================
# 🚀 MAIN
# =========================
def main():
    parser = argparse.ArgumentParser(description="USB Flasher (.img only)")
    parser.add_argument("--image", required=True, help="Path to .img file")

    args = parser.parse_args()

    if not args.image.endswith(".img"):
        print("❌ Only .img supported")
        sys.exit(1)

    if not os.path.exists(args.image):
        print("❌ Image not found")
        sys.exit(1)

    # 🔍 Auto select USB
    device = select_device()

    # ⚠️ Confirm
    confirm(device)

    # 🔥 Flash
    flash(args.image, device)

    # 🔍 Hash
    print("\n🔍 Image SHA256:")
    print(get_hash(args.image))

    print("\n🎉 Done!")

if __name__ == "__main__":
    main()
