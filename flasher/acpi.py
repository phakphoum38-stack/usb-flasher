import os
import shutil

def apply_acpi(base, hw):
    repo = "acpi_repo"
    dst = os.path.join(base, "EFI/OC/ACPI")

    tables = ["SSDT-EC.aml", "SSDT-PLUG.aml"]

    if hw["type"] == "laptop":
        tables.append("SSDT-XOSI.aml")

    for t in tables:
        src = os.path.join(repo, t)
        if os.path.exists(src):
            shutil.copy(src, dst)
