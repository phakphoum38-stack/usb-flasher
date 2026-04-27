import plistlib
import os

def validate_and_fix(efi_path, hw):
    config_path = os.path.join(efi_path, "EFI/OC/config.plist")

    if not os.path.exists(config_path):
        return False

    with open(config_path, "rb") as f:
        plist = plistlib.load(f)

    changed = False

    # 🔧 ตัวอย่าง fix
    if "PlatformInfo" not in plist:
        plist["PlatformInfo"] = {"Generic": {}}
        changed = True

    # GPU fix
    if "intel" in hw["gpu"].lower():
        plist.setdefault("DeviceProperties", {}).setdefault("Add", {})[
            "PciRoot(0x0)/Pci(0x2,0x0)"
        ] = {
            "AAPL,ig-platform-id": b'\x07\x00\x9B\x3E'
        }
        changed = True

    if changed:
        with open(config_path, "wb") as f:
            plistlib.dump(plist, f)

    return True
