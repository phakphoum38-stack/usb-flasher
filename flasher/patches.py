import plistlib
import os

def load_template(hw):
    if "amd" in hw["cpu"].lower():
        return "flasher/config_templates/amd.plist"

    if hw["type"] == "laptop":
        return "flasher/config_templates/intel_laptop.plist"

    return "flasher/config_templates/intel_desktop.plist"


def apply_patches(config_path, hw):
    with open(config_path, "rb") as f:
        plist = plistlib.load(f)

    # 🎯 SMBIOS
    if "intel" in hw["cpu"].lower():
        plist["PlatformInfo"]["Generic"]["SystemProductName"] = "iMac19,1"
    else:
        plist["PlatformInfo"]["Generic"]["SystemProductName"] = "MacPro7,1"

    # 🎯 GPU fix (basic)
    if "intel" in hw["gpu"].lower():
        plist.setdefault("DeviceProperties", {}).setdefault("Add", {})[
            "PciRoot(0x0)/Pci(0x2,0x0)"
        ] = {
            "AAPL,ig-platform-id": b'\x07\x00\x9B\x3E'
        }

    with open(config_path, "wb") as f:
        plistlib.dump(plist, f)
