import sys
import os
from flasher.rust_core import flash_with_rust

# =========================
# 🔍 SIMPLE USAGE
# =========================
def usage():
    print("USB Flash Tool (CLI)")
    print("Usage:")
    print(r"  python flasher.py <image.img> \\.\PhysicalDriveX")
    print("")
    print("Example:")
    print(r"  python flasher.py macos.img \\.\PhysicalDrive1")


# =========================
# 🚀 MAIN
# =========================
def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    image = sys.argv[1]
    device = sys.argv[2]

    # =========================
    # BASIC CHECK
    # =========================
    if not os.path.exists(image):
        print("❌ Image not found")
        sys.exit(1)

    if not image.endswith(".img"):
        print("❌ Only .img supported")
        sys.exit(1)

    print("=== USB Flash Tool ===")
    print("Image :", image)
    print("Device:", device)
    print("")

    # =========================
    # PROGRESS (console)
    # =========================
    def progress(p, s):
        sys.stdout.write(f"\r{p}% | {s} MB/s")
        sys.stdout.flush()

    # =========================
    # FLASH (RUST ENGINE)
    # =========================
    try:
        flash_with_rust(image, device, progress)
        print("\n✅ Done")

    except Exception as e:
        print("\n❌ Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
