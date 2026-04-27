import os
import shutil
from flasher.utils import resource_path

def apply_acpi(base_path, hw):
    repo = resource_path("acpi_repo")
    dst = os.path.join(base_path, "EFI/OC/ACPI")

    os.makedirs(dst, exist_ok=True)

    files = ["SSDT-EC.aml", "SSDT-PLUG.aml"]

    if hw["type"] == "laptop":
        files.append("SSDT-XOSI.aml")

    for f in files:
        src = os.path.join(repo, f)
        if os.path.exists(src):
            shutil.copy(src, dst)
