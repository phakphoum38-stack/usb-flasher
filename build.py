import PyInstaller.__main__

PyInstaller.__main__.run([
    "run.py",
    "--onefile",
    "--windowed",
    "--name=USB-Flasher-Pro",

    # 🔥 สำคัญ: กัน import หาย
    "--hidden-import=flasher.efi",
    "--hidden-import=flasher.kexts",
    "--hidden-import=flasher.hardware",
    "--hidden-import=flasher.acpi",
])
