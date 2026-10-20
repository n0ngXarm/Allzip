import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from allzip.core import compress_item, resolve_destination, get_human_size

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

    def test_human_size(self):
        self.assertEqual(get_human_size(500), "500.0 B")
        self.assertEqual(get_human_size(2048), "2.0 KB")
        self.assertEqual(get_human_size(1048576 * 5), "5.0 MB")

    def test_resolve_destination_auto_rename(self):
        sample = os.path.join(self.test_dir, "testfile.txt")
        Path(sample).touch()
        dest1, overwrite1 = resolve_destination(sample, auto_rename=True)
        self.assertEqual(dest1, os.path.join(self.test_dir, "testfile.txt.zip"))
        Path(dest1).touch()

        # When already exists
        dest2, overwrite2 = resolve_destination(sample, auto_rename=True)
        self.assertEqual(dest2, os.path.join(self.test_dir, "testfile.txt (1).zip"))

if __name__ == "__main__":
    unittest.main()
