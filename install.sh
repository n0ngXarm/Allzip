#!/usr/bin/env bash
# ==============================================================================
# Allzip: 1-Click ZIP Compressor Installer
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"
NAUTILUS_SCRIPTS_DIR="${HOME}/.local/share/nautilus/scripts"

echo "=========================================================="
echo "          ติดตั้ง Allzip - 1-Click ZIP Compressor         "
echo "=========================================================="
echo "ตำแหน่งโปรเจกต์: ${SCRIPT_DIR}"

# 1. Create target directories
mkdir -p "${BIN_DIR}" "${APP_DIR}" "${NAUTILUS_SCRIPTS_DIR}"

# 2. Copy launcher script to ~/.local/bin/zip-folder
echo "กำลังติดตั้งคำสั่ง zip-folder ไปที่ ${BIN_DIR}..."
cp -f "${SCRIPT_DIR}/zip_folder.py" "${BIN_DIR}/zip-folder"
chmod +x "${BIN_DIR}/zip-folder"

# Also link allzip library module to ~/.local/lib/python or keep path in launcher
# In zip_folder.py we already handle SCRIPT_DIR fallback, but copying allzip pkg to ~/.local/share/allzip guarantees portability
mkdir -p "${HOME}/.local/share/allzip"
cp -rf "${SCRIPT_DIR}/allzip" "${HOME}/.local/share/allzip/"

cat << 'EOF' > "${BIN_DIR}/zip-folder"
#!/usr/bin/env python3
import os
import sys

# Ensure allzip is accessible
LOCAL_SHARE = os.path.expanduser("~/.local/share/allzip")
if os.path.exists(LOCAL_SHARE) and LOCAL_SHARE not in sys.path:
    sys.path.insert(0, LOCAL_SHARE)

from allzip.core import compress_item, get_human_size
from allzip.notify import send_notification
import shutil
import subprocess

def main():
    raw_targets = []
    nautilus_paths = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').strip()
    if nautilus_paths:
        raw_targets = [p.strip() for p in nautilus_paths.splitlines() if p.strip()]
    elif len(sys.argv) > 1:
        raw_targets = [p.strip() for p in sys.argv[1:] if p.strip()]

    if not raw_targets:
        if shutil.which('zenity') and os.environ.get('DISPLAY'):
            res = subprocess.run([
                'zenity', '--file-selection',
                '--multiple',
                '--separator=|',
                '--title=เลือกไฟล์หรือโฟลเดอร์ที่ต้องการบีบอัดเป็น ZIP'
            ], capture_output=True, text=True)
            if res.returncode != 0 or not res.stdout.strip():
                return 0
            raw_targets = [p.strip() for p in res.stdout.strip().split('|') if p.strip()]
        else:
            print("Usage: zip-folder <file_or_directory_1> [file_or_directory_2 ...]")
            return 1

    if not raw_targets:
        return 0

    success_items = []
    errors = []

    for item in raw_targets:
        success, info = compress_item(item)
        if success:
            zip_path, final_size = info
            success_items.append((zip_path, final_size))
        elif info != "ยกเลิกโดยผู้ใช้":
            errors.append(f"{os.path.basename(item)}: {info}")

    if success_items:
        if len(success_items) == 1:
            z_path, z_size = success_items[0]
            msg = f"ไฟล์: {os.path.basename(z_path)}\nขนาด: {get_human_size(z_size)}\nตำแหน่ง: {os.path.dirname(z_path)}"
            send_notification("Allzip: บีบอัดสำเร็จ", msg)
        else:
            msg = f"สร้างไฟล์ ZIP สำเร็จทั้งหมด {len(success_items)} รายการ"
            send_notification("Allzip: บีบอัดสำเร็จ", msg)

    if errors:
        if shutil.which('zenity') and os.environ.get('DISPLAY'):
            subprocess.run([
                'zenity', '--error',
                '--title=บีบอัดไม่สำเร็จบางรายการ',
                '--text=' + '\n'.join(errors)
            ])
        else:
            print("\n".join(errors), file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
EOF
chmod +x "${BIN_DIR}/zip-folder"

# 3. Install desktop launcher
echo "กำลังติดตั้ง Desktop Application..."
cp -f "${SCRIPT_DIR}/allzip.desktop" "${APP_DIR}/allzip.desktop"

# 4. Install Nautilus Script
echo "กำลังเชื่อมต่อเข้ากับเมนูคลิกขวา Nautilus..."
NAUTILUS_SCRIPT="${NAUTILUS_SCRIPTS_DIR}/Allzip"
cat << 'EOF' > "${NAUTILUS_SCRIPT}"
#!/usr/bin/env bash
# Nautilus script for 1-click Allzip compression
exec "${HOME}/.local/bin/zip-folder" "$@"
EOF
chmod +x "${NAUTILUS_SCRIPT}"

# Remove any legacy aliases to keep menu clean
rm -f "${NAUTILUS_SCRIPTS_DIR}/บีบอัดเป็น ZIP"
rm -f "${NAUTILUS_SCRIPTS_DIR}/Compress to ZIP"

if which update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${APP_DIR}" 2>/dev/null || true
fi

echo "=========================================================="
echo "ติดตั้ง Allzip เรียบร้อยแล้ว"
echo ""
echo "วิธีใช้งาน:"
echo "1. ในตัวจัดการไฟล์ (Nautilus): คลิกขวาที่ไฟล์หรือโฟลเดอร์ -> Scripts -> 'Allzip'"
echo "2. ผ่านเมนูแอปพลิเคชัน: ค้นหา 'Allzip' ใน Application Menu"
echo "3. ผ่านคำสั่ง Terminal: zip-folder <path>"
echo "=========================================================="

if which notify-send >/dev/null 2>&1; then
    notify-send -a "Allzip" -i "package-x-generic" "Allzip" "ติดตั้ง Allzip เรียบร้อยแล้ว พร้อมใช้งานทันที"
fi
