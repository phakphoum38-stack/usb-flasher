OutFile "USBFlashToolPro-Setup.exe"
InstallDir $PROGRAMFILES\USBFlashToolPro

Section
  SetOutPath $INSTDIR
  File "dist\USBFlashToolPro.exe"
  CreateShortcut "$DESKTOP\USBFlashToolPro.lnk" "$INSTDIR\USBFlashToolPro.exe"
SectionEnd
