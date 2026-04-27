import os
import shutil
from flasher.utils import resource_path

def install_kexts(base_path, platform_type):
    kext_repo = resource_path("kexts_repo")

    kexts = [
        "Lilu.kext",
        "VirtualSMC.kext",
        "WhateverGreen.kext"
    ]

    dst = os.path.join(base_path, "EFI/OC/Kexts")
    os.makedirs(dst, exist_ok=True)

    for k in kexts:
        src = os.path.join(kext_repo, k)

        if os.path.exists(src):
            shutil.copytree(src, os.path.join(dst, k), dirs_exist_ok=True)
            print("✅", k)
        else:
            print("⚠️ missing", k)
