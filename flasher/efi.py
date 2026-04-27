import os
from flasher.system import get_cpu_info, detect_platform

def generate_config(base_path):
    cpu_info = get_cpu_info()
    platform_type = detect_platform(cpu_info["cpu"])

    config_path = os.path.join(base_path, "EFI/OC/config.plist")

    if platform_type == "Intel":
        smbios = "iMac19,1"
    elif platform_type == "AMD":
        smbios = "MacPro7,1"
    else:
        smbios = "iMac18,3"

    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>PlatformInfo</key>
    <dict>
        <key>Generic</key>
        <dict>
            <key>SystemProductName</key>
            <string>{smbios}</string>
        </dict>
    </dict>
</dict>
</plist>
"""

    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    with open(config_path, "w") as f:
        f.write(plist)

    print(f"✅ Config generated for {platform_type}")
