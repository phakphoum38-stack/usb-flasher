import PyInstaller.__main__

PyInstaller.__main__.run([
    "run.py",
    "--onefile",
    "--windowed",
    "--name=USB-Flasher-Pro",

    # 🔥 CORE modules
    "--hidden-import=flasher.efi",
    "--hidden-import=flasher.kexts",
    "--hidden-import=flasher.hardware",
    "--hidden-import=flasher.acpi",
    "--hidden-import=flasher.patches",

    # 📦 DATA FOLDERS (สำคัญมาก)
    "--add-data=kexts_repo;kexts_repo",
    "--add-data=acpi_repo;acpi_repo",
    "--add-data=OpenCore;OpenCore",
])
