!include "MUI2.nsh"

Name "USB Flash Tool Pro"
OutFile "USBFlashToolPro-Setup.exe"
InstallDir "$PROGRAMFILES\USBFlashToolPro"
RequestExecutionLevel admin

# =========================
# ICON
# =========================
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

# =========================
# UI PAGES
# =========================
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# =========================
# UNINSTALL UI
# =========================
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

# =========================
# INSTALL SECTION
# =========================
Section "Install"

  SetOutPath "$INSTDIR"

  File "dist\USBFlashToolPro.exe"

  # Start Menu
  CreateDirectory "$SMPROGRAMS\USB Flash Tool Pro"
  CreateShortcut "$SMPROGRAMS\USB Flash Tool Pro\USB Flash Tool Pro.lnk" "$INSTDIR\USBFlashToolPro.exe"

  # Desktop shortcut
  CreateShortcut "$DESKTOP\USB Flash Tool Pro.lnk" "$INSTDIR\USBFlashToolPro.exe"

  # Uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"

SectionEnd

# =========================
# UNINSTALL
# =========================
Section "Uninstall"

  Delete "$INSTDIR\USBFlashToolPro.exe"
  Delete "$INSTDIR\uninstall.exe"

  Delete "$DESKTOP\USB Flash Tool Pro.lnk"
  Delete "$SMPROGRAMS\USB Flash Tool Pro\USB Flash Tool Pro.lnk"

  RMDir "$SMPROGRAMS\USB Flash Tool Pro"
  RMDir "$INSTDIR"

SectionEnd
