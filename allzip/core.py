import os
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

def get_human_size(num_bytes: int) -> str:
    val = float(num_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if val < 1024.0:
            return f"{val:.1f} {unit}"
        val /= 1024.0
    return f"{val:.1f} TB"

def get_dir_size_and_count(path: str) -> tuple:
    total_size = 0
    total_files = 0
    try:
        for root, dirs, files in os.walk(path, onerror=lambda e: None):
            total_files += len(files)
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
                except OSError:
                    pass
    except OSError:
        pass
    return total_size, total_files

def resolve_destination(target_path: str, auto_rename: bool = False) -> tuple:
    parent_dir = os.path.dirname(target_path)
    base_name = os.path.basename(target_path.rstrip('/'))
    zip_name = f"{base_name}.zip"
    zip_path = os.path.join(parent_dir, zip_name)

    if not os.path.exists(zip_path):
        return zip_path, False

    if auto_rename:
        counter = 1
        while True:
            candidate = os.path.join(parent_dir, f"{base_name} ({counter}).zip")
            if not os.path.exists(candidate):
                return candidate, False
            counter += 1

    # File already exists: prompt user with Zenity if display available
    if shutil.which('zenity') and os.environ.get('DISPLAY'):
        cmd = [
            'zenity', '--question',
            '--title=พบไฟล์ชื่อซ้ำ',
            f'--text=มีไฟล์ "{zip_name}" อยู่แล้วในโฟลเดอร์นี้\n\nต้องการเขียนทับ หรือบันทึกเป็นชื่อใหม่?',
            '--ok-label=เขียนทับ',
            '--cancel-label=ยกเลิก',
            '--extra-button=สร้างชื่อใหม่'
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if 'สร้างชื่อใหม่' in res.stdout:
            counter = 1
            while True:
                candidate = os.path.join(parent_dir, f"{base_name} ({counter}).zip")
                if not os.path.exists(candidate):
                    return candidate, False
                counter += 1
        elif res.returncode == 0:
            return zip_path, True  # Overwrite
        else:
            return None, False  # Cancel

    # Fallback to auto-rename if no GUI
    counter = 1
    while True:
        candidate = os.path.join(parent_dir, f"{base_name} ({counter}).zip")
        if not os.path.exists(candidate):
            return candidate, False
        counter += 1

def _compress_python_fallback(target: str, zip_path: str, is_dir: bool, progress_proc=None):
    """Fallback pure-Python zipfile compression with Zip64 and permission resilience."""
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        if is_dir:
            base_dir = Path(target)
            for root, dirs, files in os.walk(target, onerror=lambda e: None):
                if progress_proc and progress_proc.poll() is not None and progress_proc.returncode != 0:
                    raise InterruptedError("ยกเลิกโดยผู้ใช้")
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        arcname = dir_path.relative_to(base_dir.parent)
                        zf.write(dir_path, str(arcname))
                    except (PermissionError, OSError):
                        continue
                for file_name in files:
                    file_path = Path(root) / file_name
                    try:
                        if not file_path.is_file():
                            continue
                        arcname = file_path.relative_to(base_dir.parent)
                        zf.write(file_path, str(arcname))
                    except (PermissionError, OSError):
                        continue
        else:
            zf.write(target, os.path.basename(target))

def compress_item(target: str, auto_rename: bool = False, skip_existing_zip: bool = False) -> tuple:
    target = os.path.abspath(target.rstrip('/'))
    if not os.path.exists(target):
        return False, f"ไม่พบไฟล์หรือโฟลเดอร์: {target}"

    if not os.path.isdir(target) and target.lower().endswith('.zip') and skip_existing_zip:
        return False, "เป็นไฟล์ ZIP อยู่แล้ว (ข้ามการบีบอัดซ้ำ)"

    parent_dir = os.path.dirname(target)
    base_name = os.path.basename(target)

    zip_path, overwrite = resolve_destination(target, auto_rename=auto_rename)
    if not zip_path:
        return False, "ยกเลิกโดยผู้ใช้"

    if overwrite and os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except OSError as e:
            return False, f"ไม่สามารถลบไฟล์เดิมเพื่อเขียนทับได้: {e}"

    is_dir = os.path.isdir(target)

    # Progress dialog check for large items (> 25MB or > 50 files)
    progress_proc = None
    if is_dir and shutil.which('zenity') and os.environ.get('DISPLAY'):
        size, count = get_dir_size_and_count(target)
        if size > 25 * 1024 * 1024 or count > 50:
            try:
                progress_proc = subprocess.Popen([
                    'zenity', '--progress',
                    '--title=Allzip: กำลังบีบอัดเป็น ZIP',
                    f'--text=กำลังบีบอัด "{base_name}" ({get_human_size(size)})...\nกรุณารอสักครู่ (กดยกเลิกได้หากต้องการหยุด)',
                    '--pulsate',
                    '--auto-close'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

    try:
        # Determine best available compression engine:
        # 1. 7-Zip: Ultra-fast multi-threaded ZIP creation (-mmt=on, -mx=1)
        # 2. System zip (Info-ZIP): Reliable standard CLI (-1)
        # 3. Pure Python zipfile fallback
        engine = None
        cmd = None
        acceptable_returncodes = (0,)

        if shutil.which('7z'):
            engine = '7z'
            # -tzip: standard ZIP archive
            # -mx=1: fast compression (optimal for large media/mixed workloads)
            # -mmt=on: enable multi-threading on all available cores
            cmd = ['7z', 'a', '-tzip', '-mx=1', '-mmt=on', zip_path, base_name]
            # Exit code 1 indicates non-fatal warning (e.g. skipped locked/permission denied file)
            acceptable_returncodes = (0, 1)
        elif shutil.which('zip'):
            engine = 'zip'
            cmd = ['zip', '-r', '-q', '-1', zip_path, base_name] if is_dir else ['zip', '-q', '-1', zip_path, base_name]
            # Exit code 18 for Info-ZIP indicates warning (e.g. unreadable files skipped)
            acceptable_returncodes = (0, 18)

        if cmd:
            proc = subprocess.Popen(cmd, cwd=parent_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            while proc.poll() is None:
                # Check if user cancelled Zenity progress dialog
                if progress_proc and progress_proc.poll() is not None:
                    if progress_proc.returncode != 0:
                        # User clicked Cancel on Zenity
                        proc.terminate()
                        try:
                            proc.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            proc.kill()
                        if os.path.exists(zip_path):
                            try:
                                os.remove(zip_path)
                            except OSError:
                                pass
                        return False, "ยกเลิกโดยผู้ใช้"
                time.sleep(0.1)

            if proc.returncode not in acceptable_returncodes or not os.path.exists(zip_path):
                # Try python fallback if engine failed
                _compress_python_fallback(target, zip_path, is_dir, progress_proc=progress_proc)
        else:
            _compress_python_fallback(target, zip_path, is_dir, progress_proc=progress_proc)

    except InterruptedError:
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except OSError:
                pass
        return False, "ยกเลิกโดยผู้ใช้"
    except Exception as e:
        return False, f"ข้อผิดพลาดระหว่างบีบอัด: {e}"
    finally:
        if progress_proc and progress_proc.poll() is None:
            try:
                progress_proc.terminate()
            except Exception:
                pass

    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
        final_size = os.path.getsize(zip_path)
        return True, (zip_path, final_size)
    else:
        return False, "ไม่พบไฟล์ ZIP หลังการบีบอัด"
