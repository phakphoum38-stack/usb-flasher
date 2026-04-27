import os
import shutil

from flasher.system import get_cpu_info, detect_platform
from flasher.kexts import install_kexts


# =========================
# 📁 CREATE EFI STRUCTURE
# =========================
def create_structure(base_path):
    paths = [
        "EFI/BOOT",
        "EFI/OC/ACPI",
        "EFI/OC/Kexts",
        "EFI/OC/Drivers",
        "EFI/OC/Tools"
    ]

    for p in paths:
        os.makedirs(os.path.join(base_path, p), exist_ok=True)


# =========================
# 📦 COPY OPENCORE FILES
# =========================
def copy_opencore(base_path, opencore_dir):
    if not os.path.exists(opencore_dir):
        raise Exception("❌ OpenCore folder not found")

    shutil.copytree(
        opencore_dir,
        os.path.join(base_path, "EFI"),
        dirs_exist_ok=True
    )


# =========================
# 🧠 GENERATE CONFIG
# =========================
def generate_config(base_path):
    cpu_info = get_cpu_info()
    platform_type = detect_platform(cpu_info["cpu"])

    config_path = os.path.join(base_path, "EFI/OC/config.plist")

    # 🎯 เลือก SMBIOS
    if platform_type == "Intel":
        smbios = "iMac19,1"
    elif platform_type == "AMD":
        smbios = "MacPro7,1"
    else:
        smbios = "iMac18,3"

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>PlatformInfo</key>
    <dict>
        <key>Generic</key>
        <dict>
            <key>SystemProductName</key>
            <string>{smbios}</string>
        </dict>
    </dict>

    <key>Booter</key>
    <dict>
        <key>Quirks</key>
        <dict>
            <key>EnableSafeModeSlide</key>
            <true/>
        </dict>
    </dict>

</dict>
</plist>
"""

    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    with open(config_path, "w") as f:
        f.write(plist)

    print(f"🧠 Config generated for {platform_type}")


# =========================
# 🔌 INSTALL KEXTS
# =========================
def setup_kexts(base_path):
    cpu_info = get_cpu_info()
    platform_type = detect_platform(cpu_info["cpu"])

    install_kexts(base_path, platform_type)


# =========================
# 🚀 BUILD EFI (MAIN)
# =========================
def build_efi(output_dir, opencore_dir):
    print("⚙️ Building EFI...")

    # 1. สร้างโครง
    create_structure(output_dir)

    # 2. copy OpenCore
    copy_opencore(output_dir, opencore_dir)

    # 3. config.plist
    generate_config(output_dir)

    # 4. install kexts
    setup_kexts(output_dir)

    print("✅ EFI build complete")
