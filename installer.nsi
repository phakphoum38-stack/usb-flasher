; =========================
; USB Flash Tool Pro Installer
; Enterprise Level
; =========================

!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"

!define APPNAME "USB Flash Tool Pro"
!define COMPANY "FlashForge"
!define VERSION "1.0.0"
!define EXE "USBFlashToolPro.exe"

Name "${APPNAME} ${VERSION}"
OutFile "USBFlashToolPro-Setup.exe"
InstallDir "$PROGRAMFILES64\${APPNAME}"
InstallDirRegKey HKLM "Software\${APPNAME}" "Install_Dir"
RequestExecutionLevel admin

# =========================
# ICON / BRANDING
# =========================
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

BrandingText "FlashForge Installer"

# =========================
# UI MODERN
# =========================
!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\${EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "Launch USB Flash Tool Pro"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

# =========================
# INSTALL SECTION
# =========================
Section "Main"

  SetOutPath "$INSTDIR"

  ; Copy main EXE
  File "dist\${EXE}"

  ; Save install path
  WriteRegStr HKLM "Software\${APPNAME}" "Install_Dir" "$INSTDIR"

  ; Add uninstall info
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANY}"

  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${EXE}"
  CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXE}"

  ; Write uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"

SectionEnd

# =========================
# OPTIONAL: AUTO UPDATE FILE
# =========================
Section "Config"

  SetOutPath "$INSTDIR"
  FileOpen $0 "$INSTDIR\config.json" w
  FileWrite $0 '{"auto_update": true}'
  FileClose $0

SectionEnd

# =========================
# UNINSTALL
# =========================
Section "Uninstall"

  ; Remove files
  Delete "$INSTDIR\${EXE}"
  Delete "$INSTDIR\config.json"
  Delete "$INSTDIR\uninstall.exe"

  ; Remove shortcuts
  Delete "$DESKTOP\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"

  ; Remove folders
  RMDir "$SMPROGRAMS\${APPNAME}"
  RMDir "$INSTDIR"

  ; Remove registry
  DeleteRegKey HKLM "Software\${APPNAME}"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

SectionEnd

# =========================
# PRE-INSTALL CHECK
# =========================
Function .onInit
  ; Prevent install without admin
  UserInfo::GetAccountType
  Pop $0
  ${If} $0 != "admin"
    MessageBox MB_ICONSTOP "Please run installer as Administrator."
    Abort
  ${EndIf}
FunctionEnd
