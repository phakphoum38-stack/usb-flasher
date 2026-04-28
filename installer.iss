[Setup]
AppName=USB Flasher Pro
AppVersion=1.0.0
DefaultDirName={pf}\USBFlasher
OutputDir=dist
OutputBaseFilename=USBFlasherInstaller

[Files]
Source: "dist\USB-Flasher-Pro.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\USB Flasher"; Filename: "{app}\USB-Flasher-Pro.exe"

[Run]
Filename: "{app}\USB-Flasher-Pro.exe"; Description: "Run USB Flasher"; Flags: nowait postinstall
