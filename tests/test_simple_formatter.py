import unittest
from src.implementations.SimpleFormatter import SimpleFormatter

class TestSimpleFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = SimpleFormatter()
    
    def test_empty_matches(self):
        """空のマッチリストの場合のテスト"""
        matches = []
        result = self.formatter.format(matches)
        self.assertEqual(result, "マッチする結果は見つかりませんでした。")
    
    def test_single_line_match(self):
        """単一行マッチのフォーマットテスト"""
        matches = [
            ("/path/to/file.py", 12, 12, "print(\"Hello World\")"),
            ("/path/to/another.py", 5, 5, "def test_func():"),
        ]
        result = self.formatter.format(matches)
        expected = "/path/to/file.py:12-12 print(\"Hello World\")\n/path/to/another.py:5-5 def test_func():"
        self.assertEqual(result, expected)
    
    def test_multi_line_match(self):
        """複数行マッチのフォーマットテスト"""
        matches = [
            ("/path/to/file.py", 20, 22, "def func():\n    print(\"test\")\n    return True"),
            ("/path/to/another.py", 8, 10, "class Test:\n    def __init__(self):\n        pass"),
        ]
        result = self.formatter.format(matches)
        expected = "/path/to/file.py:20-22 def func()...\n/path/to/another.py:8-10 class Test:..."
        self.assertEqual(result, expected)
    
    def test_mixed_line_match(self):
        """単一行と複数行が混在するマッチのフォーマットテスト"""
        matches = [
            ("/path/to/file.py", 12, 12, "print(\"Hello World\")"),
            ("/path/to/another.py", 8, 10, "class Test:\n    def __init__(self):\n        pass"),
        ]
        result = self.formatter.format(matches)
        expected = "/path/to/file.py:12-12 print(\"Hello World\")\n/path/to/another.py:8-10 class Test:..."
        self.assertEqual(result, expected)
    
    def test_japanese_content(self):
        """日本語コンテンツのフォーマットテスト"""
        matches = [
            ("/path/to/file.txt", 1, 1, "これは日本語のテストです。"),
            ("/path/to/another.txt", 3, 5, "複数行の\n日本語\nテスト"),
        ]
        result = self.formatter.format(matches)
        expected = "/path/to/file.txt:1-1 これは日本語のテストです。\n/path/to/another.txt:3-5 複数行の..."
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)
