#!/usr/bin/env bash
# Uninstaller for Allzip
set -e

echo "🗑️  กำลังถอนการติดตั้ง Allzip..."

rm -f "${HOME}/.local/bin/zip-folder"
rm -f "${HOME}/.local/share/applications/allzip.desktop"
rm -f "${HOME}/.local/share/nautilus/scripts/Allzip"
rm -f "${HOME}/.local/share/nautilus/scripts/บีบอัดเป็น ZIP"
rm -f "${HOME}/.local/share/nautilus/scripts/Compress to ZIP"
rm -rf "${HOME}/.local/share/allzip"

if which update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${HOME}/.local/share/applications" 2>/dev/null || true
fi

echo "✅ ถอนการติดตั้ง Allzip เรียบร้อยแล้ว"

if which notify-send >/dev/null 2>&1; then
    notify-send -a "Allzip" "Allzip" "ถอนการติดตั้งเรียบร้อยแล้ว"
fi
