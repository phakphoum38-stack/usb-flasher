# usb-flasher
::writing{variant="standard" id="84321"}
# USB Flasher (CLI)

Simple USB flasher for .img files (Phase 1)

## ⚠️ WARNING
This tool will ERASE your disk completely. Use at your own risk.

## Features
- Flash .img to USB
- Cross-platform (Windows / Linux)
- Simple CLI

## Usage

### Windows
python flasher.py --image file.img --device \\.\PhysicalDrive1

### Linux
sudo python flasher.py --image file.img --device /dev/sdb

## Roadmap
- [ ] Progress bar UI
- [ ] Device auto-detect
- [ ] Verify (
