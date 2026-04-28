#!/bin/sh

echo "========================="
echo "AUTO VERSION BUMP SYSTEM"
echo "========================="

cd usb-flasher || exit

# =========================
# READ VERSION
# =========================
version=$(cat VERSION)

echo "Current version: $version"

# =========================
# SPLIT VERSION
# =========================
major=$(echo $version | cut -d. -f1)
minor=$(echo $version | cut -d. -f2)
patch=$(echo $version | cut -d. -f3)

# =========================
# BUMP PATCH VERSION
# =========================
patch=$((patch + 1))
new_version="$major.$minor.$patch"

echo "New version: $new_version"

# =========================
# SAVE VERSION
# =========================
echo $new_version > VERSION

# =========================
# GIT OPERATIONS
# =========================
git add .
git commit -m "release $new_version"

git tag "v$new_version"

git push origin main
git push origin "v$new_version"

echo "========================="
echo "RELEASE DONE: v$new_version"
echo "========================="
