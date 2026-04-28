#!/bin/sh

echo "Auto Release Pipeline"

cd usb-flasher || exit

git add .
git commit -m "auto release"

# version auto (ง่าย ๆ)
version="v1.0.0"

git tag $version

git push origin main
git push origin $version

echo "Release triggered: $version"
