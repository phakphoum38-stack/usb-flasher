import requests
import zipfile
import os

API = "https://your-api.com/fix"

def cloud_fix(efi_path, hw):
    zip_path = "efi.zip"

    # zip EFI
    with zipfile.ZipFile(zip_path, "w") as z:
        for root, _, files in os.walk(efi_path):
            for f in files:
                full = os.path.join(root, f)
                z.write(full)

    # ส่งไป server
    files = {"file": open(zip_path, "rb")}
    data = {"hw": str(hw)}

    res = requests.post(API, files=files, data=data)

    if res.status_code == 200:
        with open("fixed.zip", "wb") as f:
            f.write(res.content)

        print("☁️ Cloud fix applied")
