#!/usr/bin/env bash
set -e

# Run this on your own computer with internet access.
# It pulls the source repos into a temporary folder for manual merge.

mkdir -p source_repos
cd source_repos

git clone https://github.com/Ag230602/LAB_6.git || true
git clone https://github.com/Ag230602/LAB_7.git || true
git clone https://github.com/Ag230602/lab_8.git || true
git clone https://github.com/Ag230602/lab_9.git || true

echo "Downloaded source repositories into source_repos/"
echo "Now copy the needed files into ../integrated_system/ according to ../MERGE_MAP.md"
