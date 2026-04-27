import subprocess
import shutil
import os

def has_cmd(cmd):
    return shutil.which(cmd) is not None

def convert_with_7z(dmg_path):
    print("📦 Trying 7-Zip (primary)...")

    out_dir = dmg_path + "_extract"
    os.makedirs(out_dir, exist_ok=True)

    try:
        subprocess.run(
            ["7z", "x", dmg_path, f"-o{out_dir}"],
            check=True
        )

        # 🔍 หาไฟล์ .img
        for root, _, files in os.walk(out_dir):
            for f in files:
                if f.lower().endswith(".img"):
                    img_path = os.path.join(root, f)
                    print(f"✅ Found IMG: {img_path}")
                    return img_path

        raise Exception("No .img found after extraction")

    except Exception as e:
        print(f"⚠️ 7-Zip failed: {e}")
        return None


def convert_with_dmg2img(dmg_path):
    print("🍎 Trying dmg2img (fallback)...")

    img_path = dmg_path.replace(".dmg", ".img")

    subprocess.run(
        ["dmg2img", dmg_path, img_path],
        check=True
    )

    return img_path


def convert_dmg(dmg_path):
    # 🔥 Priority 1: 7z
    if has_cmd("7z"):
        result = convert_with_7z(dmg_path)
        if result:
            return result

    # 🔥 Priority 2: dmg2img
    if has_cmd("dmg2img"):
        return convert_with_dmg2img(dmg_path)

    raise Exception("❌ No converter available (install 7z or dmg2img)")
