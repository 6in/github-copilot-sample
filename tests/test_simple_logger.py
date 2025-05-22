import unittest
import re
from src.implementations.SimpleLogger import SimpleLogger, LogLevel

class TestSimpleLogger(unittest.TestCase):
    def setUp(self):
        # テスト用に標準出力への出力を無効化したロガーを作成
        self.logger = SimpleLogger(output_enabled=False)
        
    def test_default_level(self):
        """デフォルトログレベル（INFO）のテスト"""
        # デフォルトはINFOレベル
        self.assertEqual(self.logger.level, LogLevel.INFO)
        
        # INFO: 出力される
        self.logger.info("This is an info message")
        info_logs = self.logger.get_logs("INFO")
        self.assertEqual(len(info_logs), 1)
        self.assertIn("INFO", info_logs[0])
        self.assertIn("This is an info message", info_logs[0])
        
        # DEBUG: 出力されない（デフォルトレベルINFOより詳細なため）
        self.logger.debug("This is a debug message")
        debug_logs = self.logger.get_logs("DEBUG")
        self.assertEqual(len(debug_logs), 0)
        
        # ERROR: 常に出力される
        self.logger.error("This is an error message")
        error_logs = self.logger.get_logs("ERROR")
        self.assertEqual(len(error_logs), 1)
        self.assertIn("ERROR", error_logs[0])
        self.assertIn("This is an error message", error_logs[0])
        
    def test_debug_level(self):
        """DEBUGログレベルのテスト"""
        # ログレベルをDEBUGに設定
        self.logger.set_level(LogLevel.DEBUG)
        
        # INFO: 出力される
        self.logger.info("This is an info message")
        info_logs = self.logger.get_logs("INFO")
        self.assertEqual(len(info_logs), 1)
        self.assertIn("INFO", info_logs[0])
        
        # DEBUG: 出力される
        self.logger.debug("This is a debug message")
        debug_logs = self.logger.get_logs("DEBUG")
        self.assertEqual(len(debug_logs), 1)
        self.assertIn("DEBUG", debug_logs[0])
        self.assertIn("This is a debug message", debug_logs[0])
        
    def test_error_level(self):
        """ERRORログレベルのテスト"""
        # ログレベルをERRORに設定
        self.logger.set_level(LogLevel.ERROR)
        
        # INFO: 出力されない
        self.logger.info("This is an info message")
        info_logs = self.logger.get_logs("INFO")
        self.assertEqual(len(info_logs), 0)
        
        # DEBUG: 出力されない
        self.logger.debug("This is a debug message")
        debug_logs = self.logger.get_logs("DEBUG")
        self.assertEqual(len(debug_logs), 0)
        
        # ERROR: 常に出力される
        self.logger.error("This is an error message")
        error_logs = self.logger.get_logs("ERROR")
        self.assertEqual(len(error_logs), 1)
        self.assertIn("ERROR", error_logs[0])
        self.assertIn("This is an error message", error_logs[0])
        
    def test_log_format(self):
        """ログフォーマットのテスト"""
        log_line = self.logger.info("Test message")
        
        # 形式: [INFO] [yyyy-mm-dd HH:MM:SS] メッセージ
        self.assertRegex(log_line, r"^\[INFO\] \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Test message$")

if __name__ == '__main__':
    unittest.main()
        
    def test_default_level(self):
        """デフォルトログレベル（INFO）のテスト"""
        # デフォルトはINFOレベル
        self.assertEqual(self.logger.level, LogLevel.INFO)
        
        # INFO: 出力される
        self.logger.info("This is an info message")
        self.assertIn("INFO", self.held_stdout.getvalue())
        self.assertIn("This is an info message", self.held_stdout.getvalue())
        
        # DEBUG: 出力されない（デフォルトレベルINFOより詳細なため）
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.logger.debug("This is a debug message")
        self.assertEqual("", self.held_stdout.getvalue())
        
        # ERROR: 常に出力される（標準エラー出力に）
        self.logger.error("This is an error message")
        self.assertIn("ERROR", self.held_stderr.getvalue())
        self.assertIn("This is an error message", self.held_stderr.getvalue())
        
    def test_debug_level(self):
        """DEBUGログレベルのテスト"""
        # ログレベルをDEBUGに設定
        self.logger.set_level(LogLevel.DEBUG)
        
        # INFO: 出力される
        self.logger.info("This is an info message")
        self.assertIn("INFO", self.held_stdout.getvalue())
        
        # DEBUG: 出力される
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.logger.debug("This is a debug message")
        self.assertIn("DEBUG", self.held_stdout.getvalue())
        self.assertIn("This is a debug message", self.held_stdout.getvalue())
        
    def test_error_level(self):
        """ERRORログレベルのテスト"""
        # ログレベルをERRORに設定
        self.logger.set_level(LogLevel.ERROR)
        
        # INFO: 出力されない
        self.logger.info("This is an info message")
        self.assertEqual("", self.held_stdout.getvalue())
        
        # DEBUG: 出力されない
        self.logger.debug("This is a debug message")
        self.assertEqual("", self.held_stdout.getvalue())
        
        # ERROR: 常に出力される
        self.logger.error("This is an error message")
        self.assertIn("ERROR", self.held_stderr.getvalue())
        self.assertIn("This is an error message", self.held_stderr.getvalue())
        
    def test_log_format(self):
        """ログフォーマットのテスト"""
        self.logger.info("Test message")
        
        log_line = self.held_stdout.getvalue().strip()
        
        # 形式: [INFO] [yyyy-mm-dd HH:MM:SS] メッセージ
        self.assertRegex(log_line, r"^\[INFO\] \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Test message$")

if __name__ == '__main__':
    unittest.main()
