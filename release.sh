#!/bin/sh

echo "========================="
echo "AUTO VERSION BUMP SYSTEM"
echo "========================="

version_file="VERSION"

if [ ! -f "$version_file" ]; then
  echo "1.0.0" > "$version_file"
fi

version=$(cat "$version_file")

major=$(echo "$version" | cut -d. -f1)
minor=$(echo "$version" | cut -d. -f2)
patch=$(echo "$version" | cut -d. -f3)

patch=$((patch + 1))
new_version="$major.$minor.$patch"

echo "$new_version" > "$version_file"

echo "Version: $new_version"

git add .
git commit -m "release $new_version"

git tag "v$new_version"

git push origin main
git push origin "v$new_version"
