import sys
import os
import time

from flasher.rust_core import flash_with_rust
from flasher.formats import prepare_image
from flasher.verify import quick_verify
from flasher.devices import get_usb_devices


# =========================
# 🔍 USAGE
# =========================
def usage():
    print("USB Flash Tool (CLI)")
    print("Usage:")
    print(r"  python flasher.py <image> <device>")
    print("")
    print("Examples:")
    print(r"  python flasher.py macos.img \\.\PhysicalDrive1")
    print(r"  python flasher.py ubuntu.iso /dev/sdb")
    print("")
    print("Options:")
    print("  --list     Show USB devices")
    print("  --help     Show this help")


# =========================
# 📦 LIST DEVICES
# =========================
def list_devices():
    devs = get_usb_devices()

    if not devs:
        print("❌ No USB devices found")
        return

    print("\n📦 USB Devices:\n")
    for i, d in enumerate(devs):
        print(f"[{i}] {d['path']} | {d['model']} | {d.get('size','')}")
    print("")


# =========================
# 🚀 MAIN
# =========================
def main():

    # =========================
    # HELP
    # =========================
    if "--help" in sys.argv or "-h" in sys.argv:
        usage()
        sys.exit(0)

    # =========================
    # LIST USB
    # =========================
    if "--list" in sys.argv:
        list_devices()
        sys.exit(0)

    # =========================
    # ARGS
    # =========================
    if len(sys.argv) < 3:
        usage()
        sys.exit(0)  # ✅ ไม่ error แล้ว

    image = sys.argv[1]
    device = sys.argv[2]

    # =========================
    # CHECK IMAGE
    # =========================
    if not os.path.exists(image):
        print("❌ Image not found")
        sys.exit(1)

    # =========================
    # PREPARE IMAGE (ISO/DMG FIX)
    # =========================
    print("📦 Preparing image...")
    try:
        img = prepare_image(image)
    except Exception as e:
        print("❌ Prepare failed:", e)
        sys.exit(1)

    print("Using:", img)

    # =========================
    # CONFIRM (สำคัญมาก)
    # =========================
    print("\n⚠️ WARNING: This will erase:", device)
    confirm = input("Type YES to continue: ")

    if confirm != "YES":
        print("❌ Cancelled")
        sys.exit(0)

    print("\n=== USB Flash Tool ===")
    print("Image :", img)
    print("Device:", device)
    print("")

    start_time = time.time()
    last_update = 0

    # =========================
    # PROGRESS
    # =========================
    def progress(p, s):
        nonlocal last_update

        now = time.time()
        if now - last_update < 0.05:
            return

        last_update = now

        elapsed = now - start_time
        eta = int((100 - p) * (elapsed / p)) if p > 0 else 0

        sys.stdout.write(f"\r{p}% | {s} MB/s | ETA {eta}s")
        sys.stdout.flush()

    # =========================
    # FLASH
    # =========================
    try:
        flash_with_rust(img, device, progress)

        print("\n\n🔍 Verifying...")
        ok = quick_verify(img, device)

        if ok:
            print("✅ Flash complete")
        else:
            print("❌ Verify failed")
            sys.exit(1)

    except Exception as e:
        print("\n❌ Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
