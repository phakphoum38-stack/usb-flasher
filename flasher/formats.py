import os
import subprocess
from flasher.dmg import convert_dmg


def prepare_image(path):
    original = path
    ext = path.lower().split(".")[-1]

    # =========================
    # IMG → ใช้ได้เลย
    # =========================
    if ext == "img":
        return original

    # =========================
    # ISO → convert → IMG
    # =========================
    if ext == "iso":
        out = original + ".img"

        if os.path.exists(out):
            return out

        print("📀 Converting ISO → IMG...")

        try:
            subprocess.run([
                "dd",
                f"if={original}",
                f"of={out}",
                "bs=4M"
            ], check=True)
        except:
            raise Exception("❌ ISO convert failed")

        return out

    # =========================
    # DMG → IMG
    # =========================
    if ext == "dmg":
        print("🍎 Converting DMG → IMG...")
        return convert_dmg(original)

    # =========================
    # Unsupported
    # =========================
    raise Exception("❌ Unsupported format")
