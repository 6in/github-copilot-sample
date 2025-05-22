import unittest
import os
import tempfile
import shutil
from src.implementations.GitignoreParser import GitignoreParser

class TestGitignoreParser(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.temp_dir = tempfile.mkdtemp()
        
        # テスト用の.gitignoreファイルを作成
        self.gitignore_path = os.path.join(self.temp_dir, ".gitignore")
        with open(self.gitignore_path, "w", encoding="utf-8") as f:
            f.write("# これはコメントです\n")
            f.write("\n")  # 空行
            f.write("*.log\n")
            f.write("build/\n")
            f.write("!important.log\n")  # 除外の例外
            f.write("/root_only.txt\n")  # ルートディレクトリのみ
            f.write("docs/**/*.md\n")    # 再帰的なパターン
        
        # テスト用のファイル構造を作成
        paths = [
            "test.log",
            "important.log",
            "root_only.txt",
            "subdir/test.log",
            "subdir/text.txt",
            "build/output.txt",
            "docs/readme.md",
            "docs/api/spec.md",
            "src/main.py"
        ]
        
        for path in paths:
            full_path = os.path.join(self.temp_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write("test content")
    
    def tearDown(self):
        # テスト用の一時ディレクトリを削除
        shutil.rmtree(self.temp_dir)
    
    def test_parse(self):
        """パターンファイルの解析テスト"""
        parser = GitignoreParser()
        patterns = parser.parse(self.gitignore_path)
        
        # コメントと空行を除いた5つのパターンが返されるはず
        self.assertEqual(len(patterns), 5)
        self.assertIn("*.log", patterns)
        self.assertIn("build/", patterns)
        self.assertIn("!important.log", patterns)
        self.assertIn("/root_only.txt", patterns)
        self.assertIn("docs/**/*.md", patterns)
    
    def test_matches(self):
        """パターンマッチングのテスト"""
        parser = GitignoreParser()
        parser.parse(self.gitignore_path)
        
        # マッチするパスのテスト
        self.assertTrue(parser.matches("test.log"))
        self.assertTrue(parser.matches("subdir/test.log"))
        self.assertTrue(parser.matches("build/output.txt"))
        self.assertTrue(parser.matches("build/subdir/file.txt"))
        self.assertTrue(parser.matches("root_only.txt"))
        self.assertTrue(parser.matches("docs/readme.md"))
        self.assertTrue(parser.matches("docs/api/spec.md"))
        
        # マッチしないパスのテスト
        self.assertFalse(parser.matches("important.log"))
        self.assertFalse(parser.matches("subdir/text.txt"))
        self.assertFalse(parser.matches("src/main.py"))
        self.assertFalse(parser.matches("subdir/root_only.txt"))
    
    def test_filter_paths(self):
        """パスのフィルタリングテスト"""
        parser = GitignoreParser()
        parser.parse(self.gitignore_path)
        
        paths = [
            "test.log",
            "important.log",
            "root_only.txt",
            "subdir/test.log",
            "subdir/text.txt",
            "build/output.txt",
            "docs/readme.md",
            "src/main.py"
        ]
        
        filtered_paths = parser.filter_paths(paths)
        
        # 除外パターンにマッチしないパスのみが残るはず
        self.assertEqual(len(filtered_paths), 3)
        self.assertIn("important.log", filtered_paths)
        self.assertIn("subdir/text.txt", filtered_paths)
        self.assertIn("src/main.py", filtered_paths)
        
        # 除外されるべきパスがないことを確認
        self.assertNotIn("test.log", filtered_paths)
        self.assertNotIn("root_only.txt", filtered_paths)
        self.assertNotIn("subdir/test.log", filtered_paths)
        self.assertNotIn("build/output.txt", filtered_paths)
        self.assertNotIn("docs/readme.md", filtered_paths)
    
    def test_nonexistent_file(self):
        """存在しないファイルのテスト"""
        parser = GitignoreParser()
        
        # 存在しないファイルではFileNotFoundErrorが発生するはず
        with self.assertRaises(FileNotFoundError):
            parser.parse(os.path.join(self.temp_dir, "nonexistent.gitignore"))
    
    def test_create_from_patterns(self):
        """パターンリストからの作成テスト"""
        patterns = ["*.log", "build/", "!important.log"]
        parser = GitignoreParser.create_from_patterns(patterns)
        
        # インスタンスが正しく作成されていることを確認
        self.assertIsNotNone(parser.spec)
        
        # パターンマッチングが正しく動作することを確認
        self.assertTrue(parser.matches("test.log"))
        self.assertTrue(parser.matches("build/output.txt"))
        self.assertFalse(parser.matches("important.log"))
        self.assertFalse(parser.matches("src/main.py"))

if __name__ == "__main__":
    unittest.main()
