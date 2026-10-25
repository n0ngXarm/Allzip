#!/usr/bin/env bash
# ==============================================================================
# Allzip: 1-Click ZIP Compressor Installer
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"
NAUTILUS_SCRIPTS_DIR="${HOME}/.local/share/nautilus/scripts"
LOCAL_SHARE_ALLZIP="${HOME}/.local/share/allzip"

echo "=========================================================="
echo "          ติดตั้ง Allzip - 1-Click ZIP Compressor         "
echo "=========================================================="
echo "ตำแหน่งโปรเจกต์: ${SCRIPT_DIR}"

# 1. Create target directories
mkdir -p "${BIN_DIR}" "${APP_DIR}" "${NAUTILUS_SCRIPTS_DIR}" "${LOCAL_SHARE_ALLZIP}"

# 2. Copy allzip library module to ~/.local/share/allzip
echo "กำลังติดตั้งโมดูล allzip ไปที่ ${LOCAL_SHARE_ALLZIP}..."
cp -rf "${SCRIPT_DIR}/allzip" "${LOCAL_SHARE_ALLZIP}/"

# 3. Copy launcher script to ~/.local/bin/zip-folder
echo "กำลังติดตั้งคำสั่ง zip-folder ไปที่ ${BIN_DIR}..."
cp -f "${SCRIPT_DIR}/zip_folder.py" "${BIN_DIR}/zip-folder"
chmod +x "${BIN_DIR}/zip-folder"

# 4. Install desktop launcher
echo "กำลังติดตั้ง Desktop Application..."
cp -f "${SCRIPT_DIR}/allzip.desktop" "${APP_DIR}/allzip.desktop"

# 5. Install Nautilus Script
echo "กำลังเชื่อมต่อเข้ากับเมนูคลิกขวา Nautilus..."
NAUTILUS_SCRIPT="${NAUTILUS_SCRIPTS_DIR}/Allzip"
cat << 'EOF' > "${NAUTILUS_SCRIPT}"
#!/usr/bin/env bash
# Nautilus script for 1-click Allzip compression
exec "${HOME}/.local/bin/zip-folder" "$@"
EOF
chmod +x "${NAUTILUS_SCRIPT}"

# Remove legacy aliases if any
rm -f "${NAUTILUS_SCRIPTS_DIR}/บีบอัดเป็น ZIP"
rm -f "${NAUTILUS_SCRIPTS_DIR}/Compress to ZIP"

if which update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${APP_DIR}" 2>/dev/null || true
fi

echo "=========================================================="
echo "ติดตั้ง Allzip เรียบร้อยแล้ว!"
echo ""
echo "วิธีใช้งาน:"
echo "1. ในตัวจัดการไฟล์ (Nautilus): คลิกขวาที่ไฟล์หรือโฟลเดอร์ -> Scripts -> 'Allzip'"
echo "2. ผ่านเมนูแอปพลิเคชัน: ค้นหา 'Allzip' ใน Application Menu"
echo "3. ผ่านคำสั่ง Terminal: zip-folder <path>"
echo "=========================================================="

if which notify-send >/dev/null 2>&1; then
    notify-send -a "Allzip" -i "package-x-generic" "Allzip" "ติดตั้ง Allzip เรียบร้อยแล้ว พร้อมใช้งานทันที"
fi
