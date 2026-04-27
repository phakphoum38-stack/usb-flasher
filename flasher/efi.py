import os
import shutil

def create_efi_structure(base_path):
    paths = [
        "EFI/BOOT",
        "EFI/OC/ACPI",
        "EFI/OC/Kexts",
        "EFI/OC/Drivers",
        "EFI/OC/Tools"
    ]

    for p in paths:
        os.makedirs(os.path.join(base_path, p), exist_ok=True)


def copy_opencore_files(base_path, source_dir):
    # source_dir = โฟลเดอร์ OpenCore ที่คุณเตรียมไว้
    shutil.copytree(source_dir, os.path.join(base_path, "EFI"), dirs_exist_ok=True)


def generate_basic_config(base_path):
    config_path = os.path.join(base_path, "EFI/OC/config.plist")

    content = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Boot</key>
    <dict>
        <key>Timeout</key>
        <integer>5</integer>
    </dict>
</dict>
</plist>
"""

    with open(config_path, "w") as f:
        f.write(content)


def build_efi(output_dir, opencore_dir):
    print("⚙️ Building EFI...")

    create_efi_structure(output_dir)
    copy_opencore_files(output_dir, opencore_dir)
    generate_basic_config(output_dir)

    print("✅ EFI ready")
