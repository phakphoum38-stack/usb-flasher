[Setup]
AppName=USB Flasher Pro
AppVersion=1.0.0
DefaultDirName={pf}\USBFlasherPro
DefaultGroupName=USB Flasher Pro
OutputDir=dist
OutputBaseFilename=USBFlasherPro_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\USB-Flasher-Pro.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\USB Flasher Pro"; Filename: "{app}\USB-Flasher-Pro.exe"
Name: "{commondesktop}\USB Flasher Pro"; Filename: "{app}\USB-Flasher-Pro.exe"

[Run]
Filename: "{app}\USB-Flasher-Pro.exe"; Description: "Launch App"; Flags: nowait postinstall
