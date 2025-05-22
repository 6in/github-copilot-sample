import unittest
from pathlib import Path
import tempfile
import os
from src.implementations.RegexMatcher import RegexMatcher

class TestRegexMatcher(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ファイルを作成
        self.temp_dir = tempfile.mkdtemp()
        
        # 単一行のテスト用ファイル
        self.single_line_file = os.path.join(self.temp_dir, "single_line.txt")
        with open(self.single_line_file, 'w', encoding='utf-8') as f:
            f.write("This is a test file for RegexMatcher.\n")
            f.write("It contains some test patterns.\n")
            f.write("Like regex pattern test.\n")
            f.write("End of file.")
        
        # 複数行のテスト用ファイル
        self.multi_line_file = os.path.join(self.temp_dir, "multi_line.txt")
        with open(self.multi_line_file, 'w', encoding='utf-8') as f:
            f.write("Start of multi-line file.\n")
            f.write("This is a\n")
            f.write("multi-line\n")
            f.write("pattern that spans\n")
            f.write("across multiple lines.\n")
            f.write("End of file.")
        
        # 日本語テキスト用ファイル
        self.japanese_file = os.path.join(self.temp_dir, "japanese.txt")
        with open(self.japanese_file, 'w', encoding='utf-8') as f:
            f.write("これは日本語のテストファイルです。\n")
            f.write("正規表現のパターンマッチをテストします。\n")
            f.write("複数行に渡る\n")
            f.write("パターンも\n")
            f.write("テストします。\n")
    
    def tearDown(self):
        # テスト終了後に一時ディレクトリを削除
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_single_line_match(self):
        matcher = RegexMatcher()
        # "test"という単語にマッチするパターン
        matches = matcher.match(self.single_line_file, r"test")
        
        # 3つのマッチが見つかるはず
        self.assertEqual(len(matches), 3)
        
        # 各マッチが正しい行にあるか確認
        self.assertEqual(matches[0][0], 1)  # 1行目のマッチ
        self.assertEqual(matches[1][0], 2)  # 2行目のマッチ
        self.assertEqual(matches[2][0], 3)  # 3行目のマッチ
        
        # 全てのマッチが単一行内であることを確認
        for start_line, end_line, _ in matches:
            self.assertEqual(start_line, end_line)
    
    def test_multi_line_match(self):
        matcher = RegexMatcher()
        # 複数行にまたがるパターン
        pattern = r"This is a\nmulti-line\npattern"
        matches = matcher.match(self.multi_line_file, pattern)
        
        # 1つのマッチが見つかるはず
        self.assertEqual(len(matches), 1)
        
        # マッチは2行目から4行目にまたがるはず
        start_line, end_line, match_text = matches[0]
        self.assertEqual(start_line, 2)
        self.assertEqual(end_line, 4)
        self.assertIn("This is a", match_text)
        self.assertIn("multi-line", match_text)
        self.assertIn("pattern", match_text)
    
    def test_japanese_text(self):
        matcher = RegexMatcher()
        # 日本語の正規表現パターン
        pattern = r"複数行に渡る\nパターンも"
        matches = matcher.match(self.japanese_file, pattern)
        
        # 1つのマッチが見つかるはず
        self.assertEqual(len(matches), 1)
        
        # マッチは3行目から4行目にまたがるはず
        start_line, end_line, match_text = matches[0]
        self.assertEqual(start_line, 3)
        self.assertEqual(end_line, 4)
        self.assertIn("複数行に渡る", match_text)
        self.assertIn("パターンも", match_text)
    
    def test_no_match(self):
        matcher = RegexMatcher()
        # ファイルに存在しないパターン
        matches = matcher.match(self.single_line_file, r"nonexistent pattern")
        
        # マッチは見つからないはず
        self.assertEqual(len(matches), 0)

if __name__ == '__main__':
    unittest.main()
