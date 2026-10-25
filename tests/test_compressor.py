import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from allzip.core import (
    compress_item,
    resolve_destination,
    get_human_size,
    _compress_python_fallback
)

class TestAllzip(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_allzip_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_compress_single_file(self):
        sample_file = os.path.join(self.test_dir, "document.txt")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("Hello World Allzip Test")

        success, info = compress_item(sample_file)
        self.assertTrue(success)
        zip_path, size = info
        self.assertTrue(os.path.exists(zip_path))
        self.assertGreater(size, 0)

        # Verify ZIP contains the file
        with zipfile.ZipFile(zip_path, "r") as zf:
            self.assertIn("document.txt", zf.namelist())

    def test_compress_folder_with_unicode(self):
        folder_path = os.path.join(self.test_dir, "เอกสารภาษาไทย")
        os.makedirs(folder_path, exist_ok=True)
        sub_file = os.path.join(folder_path, "ข้อมูลสำคัญ.txt")
        with open(sub_file, "w", encoding="utf-8") as f:
            f.write("ทดสอบเนื้อหาภาษาไทย")

        success, info = compress_item(folder_path)
        self.assertTrue(success)
        zip_path, size = info
        self.assertTrue(os.path.exists(zip_path))
        self.assertGreater(size, 0)

        # Verify ZIP contains subfile
        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = zf.namelist()
            self.assertTrue(any("ข้อมูลสำคัญ.txt" in n for n in namelist))

    def test_human_size(self):
        self.assertEqual(get_human_size(500), "500.0 B")
        self.assertEqual(get_human_size(2048), "2.0 KB")
        self.assertEqual(get_human_size(1048576 * 5), "5.0 MB")
        self.assertEqual(get_human_size(1073741824 * 3), "3.0 GB")

    def test_resolve_destination_auto_rename(self):
        sample = os.path.join(self.test_dir, "testfile.txt")
        Path(sample).touch()
        dest1, overwrite1 = resolve_destination(sample, auto_rename=True)
        self.assertEqual(dest1, os.path.join(self.test_dir, "testfile.txt.zip"))
        Path(dest1).touch()

        # When already exists
        dest2, overwrite2 = resolve_destination(sample, auto_rename=True)
        self.assertEqual(dest2, os.path.join(self.test_dir, "testfile.txt (1).zip"))

    def test_skip_existing_zip(self):
        zip_file = os.path.join(self.test_dir, "archive.zip")
        Path(zip_file).touch()

        # With skip_existing_zip=True, it should skip
        success, info = compress_item(zip_file, skip_existing_zip=True)
        self.assertFalse(success)
        self.assertEqual(info, "เป็นไฟล์ ZIP อยู่แล้ว (ข้ามการบีบอัดซ้ำ)")

    def test_python_fallback_resilience(self):
        folder = os.path.join(self.test_dir, "mixed_folder")
        os.makedirs(folder, exist_ok=True)
        good_file = os.path.join(folder, "good.txt")
        with open(good_file, "w") as f:
            f.write("I am readable")

        target_zip = os.path.join(self.test_dir, "fallback_test.zip")
        _compress_python_fallback(folder, target_zip, is_dir=True)
        self.assertTrue(os.path.exists(target_zip))
        with zipfile.ZipFile(target_zip, "r") as zf:
            self.assertTrue(any("good.txt" in n for n in zf.namelist()))

if __name__ == "__main__":
    unittest.main()
