import subprocess
import shutil
import os

def has_cmd(cmd):
    return shutil.which(cmd) is not None

def convert_dmg(dmg_path):
    img_path = dmg_path.replace(".dmg", ".img")

    # 🔥 วิธี 1: dmg2img (ดีที่สุด)
    if has_cmd("dmg2img"):
        print("🍎 Using dmg2img...")
        subprocess.run(["dmg2img", dmg_path, img_path], check=True)
        return img_path

    # 🔥 วิธี 2: 7z
    if has_cmd("7z"):
        print("📦 Using 7-Zip...")

        out_dir = dmg_path + "_extract"
        os.makedirs(out_dir, exist_ok=True)

        subprocess.run(["7z", "x", dmg_path, f"-o{out_dir}"], check=True)

        # หาไฟล์ img
        for root, _, files in os.walk(out_dir):
            for f in files:
                if f.endswith(".img"):
                    return os.path.join(root, f)

    raise Exception("❌ Cannot convert DMG (install dmg2img or 7z)")
