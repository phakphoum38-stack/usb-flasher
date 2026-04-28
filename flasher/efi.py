import os

def build_efi(efi_dir, target="OpenCore"):
    """
    Minimal EFI builder (CLEAN VERSION)
    ไม่มี kext / cloud / autofix dependency
    """

    folders = [
        "EFI/OC",
        "EFI/BOOT",
        "EFI/OC/Kexts",
        "EFI/OC/ACPI",
        "EFI/OC/Drivers",
        "EFI/OC/Resources"
    ]

    for folder in folders:
        path = os.path.join(efi_dir, folder)
        os.makedirs(path, exist_ok=True)

    # create minimal config placeholder
    config_path = os.path.join(efi_dir, "EFI/OC/config.plist")

    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("<plist version='1.0'></plist>")

    print("✅ EFI built successfully (clean mode)")
