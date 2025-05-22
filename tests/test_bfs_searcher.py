import unittest
from pathlib import Path
import tempfile
import shutil
from src.BfsSearcher import BfsSearcher

class TestBfsSearcher(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # ディレクトリ構造作成
        Path(f"{self.temp_dir}/a.txt").write_text("test a")
        Path(f"{self.temp_dir}/b.py").write_text("test b")
        sub_dir = Path(f"{self.temp_dir}/sub")
        sub_dir.mkdir()
        Path(f"{self.temp_dir}/sub/c.txt").write_text("test c")
        Path(f"{self.temp_dir}/sub/d.md").write_text("test d")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_search_all(self):
        searcher = BfsSearcher()
        files = searcher.search(Path(self.temp_dir), [], [])
        self.assertEqual(len(files), 4)

    def test_search_ext_txt(self):
        searcher = BfsSearcher()
        files = searcher.search(Path(self.temp_dir), ['.txt'], [])
        self.assertEqual(len(files), 2)
        for f in files:
            self.assertTrue(str(f).endswith('.txt'))

    def test_search_ignore(self):
        searcher = BfsSearcher()
        files = searcher.search(Path(self.temp_dir), [], ['*/sub/*'])
        self.assertEqual(len(files), 2)
        for f in files:
            self.assertFalse('sub' in str(f))

if __name__ == '__main__':
    unittest.main()
