import os
import shutil
from flasher.hardware import get_hw
from flasher.acpi import apply_acpi
from flasher.kexts import detect_kexts
from flasher.patches import load_template, apply_patches


def build_efi(out, opencore):
    print("🚀 ULTIMATE EFI BUILD")

    hw = get_hw()

    # copy OpenCore
    shutil.copytree(opencore, os.path.join(out, "EFI"), dirs_exist_ok=True)

    # ACPI
    apply_acpi(out, hw)

    # Kexts
    kext_dir = os.path.join(out, "EFI/OC/Kexts")
    os.makedirs(kext_dir, exist_ok=True)

    for k in detect_kexts(hw):
        src = os.path.join("kexts_repo", k)
        dst = os.path.join(kext_dir, k)
        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)

    # Config template
    template = load_template(hw)
    config_path = os.path.join(out, "EFI/OC/config.plist")
    shutil.copy(template, config_path)

    # Apply patches
    apply_patches(config_path, hw)

    print("✅ EFI DONE")
