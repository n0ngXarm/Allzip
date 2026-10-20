#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allzip: 1-Click ZIP Compressor
Works with Nautilus context menu, command line, or standalone file picker.
"""
import os
import sys
import shutil
import subprocess

# Ensure allzip package is on python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from allzip.core import compress_item, get_human_size
from allzip.notify import send_notification

def main():
    raw_targets = []

    # 1. Check Nautilus Script environment
    nautilus_paths = os.environ.get('NAUTILUS_SCRIPT_SELECTED_FILE_PATHS', '').strip()
    if nautilus_paths:
        raw_targets = [p.strip() for p in nautilus_paths.splitlines() if p.strip()]
    elif len(sys.argv) > 1:
        # 2. Check command line arguments / drag & drop
        raw_targets = [p.strip() for p in sys.argv[1:] if p.strip()]

    # 3. If no targets provided (e.g. launched from app launcher), open Zenity picker
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

    # Send notifications
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
