import os
import shutil

# kext library (คุณต้องเตรียมโฟลเดอร์นี้)
KEXT_LIBRARY = "kexts_repo"

BASE_KEXTS = [
    "Lilu.kext",
    "VirtualSMC.kext",
]

INTEL_KEXTS = [
    "WhateverGreen.kext",
    "IntelMausi.kext"
]

AMD_KEXTS = [
    "WhateverGreen.kext"
]

def detect_kexts(cpu_type):
    kexts = BASE_KEXTS.copy()

    if cpu_type == "Intel":
        kexts += INTEL_KEXTS
    elif cpu_type == "AMD":
        kexts += AMD_KEXTS

    return kexts


def detect_kexts(hw):
    k = ["Lilu.kext", "VirtualSMC.kext", "WhateverGreen.kext"]

    if hw["type"] == "laptop":
        k.append("VoodooPS2Controller.kext")

    if "realtek" in hw["gpu"].lower():
        k.append("RealtekRTL8111.kext")

    return k
def install_kexts(efi_path, cpu_type):
    kexts = detect_kexts(cpu_type)

    kext_dir = os.path.join(efi_path, "EFI/OC/Kexts")
    os.makedirs(kext_dir, exist_ok=True)

    for k in kexts:
        src = os.path.join(KEXT_LIBRARY, k)
        dst = os.path.join(kext_dir, k)

        if os.path.exists(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"✅ Added {k}")
        else:
            print(f"⚠️ Missing {k}")
