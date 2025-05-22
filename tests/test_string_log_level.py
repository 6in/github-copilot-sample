import unittest
from src.implementations.SimpleLogger import SimpleLogger, LogLevel

class TestStringLogLevel(unittest.TestCase):
    
    def test_string_debug_level(self):
        """文字列DEBUGログレベルのテスト"""
        logger = SimpleLogger(output_enabled=False, log_level="DEBUG")
        self.assertEqual(logger.level, LogLevel.DEBUG)
        
        # INFO: 出力される
        logger.info("This is an info message")
        info_logs = logger.get_logs("INFO")
        self.assertEqual(len(info_logs), 1)
        
        # DEBUG: 出力される
        logger.debug("This is a debug message")
        debug_logs = logger.get_logs("DEBUG")
        self.assertEqual(len(debug_logs), 1)
    
    def test_string_info_level(self):
        """文字列INFOログレベルのテスト"""
        logger = SimpleLogger(output_enabled=False, log_level="INFO")
        self.assertEqual(logger.level, LogLevel.INFO)
        
        # INFO: 出力される
        logger.info("This is an info message")
        info_logs = logger.get_logs("INFO")
        self.assertEqual(len(info_logs), 1)
        
        # DEBUG: 出力されない
        logger.debug("This is a debug message")
        debug_logs = logger.get_logs("DEBUG")
        self.assertEqual(len(debug_logs), 0)
    
    def test_string_error_level(self):
        """文字列ERRORログレベルのテスト"""
        logger = SimpleLogger(output_enabled=False, log_level="ERROR")
        self.assertEqual(logger.level, LogLevel.ERROR)
        
        # INFO: 出力されない
        logger.info("This is an info message")
        info_logs = logger.get_logs("INFO")
        self.assertEqual(len(info_logs), 0)
        
        # DEBUG: 出力されない
        logger.debug("This is a debug message")
        debug_logs = logger.get_logs("DEBUG")
        self.assertEqual(len(debug_logs), 0)
        
        # ERROR: 常に出力される
        logger.error("This is an error message")
        error_logs = logger.get_logs("ERROR")
        self.assertEqual(len(error_logs), 1)
    
    def test_invalid_string_level(self):
        """不正な文字列ログレベルのテスト（INFOにフォールバック）"""
        logger = SimpleLogger(output_enabled=False, log_level="INVALID")
        # 不正なレベルの場合はINFOにフォールバック
        self.assertEqual(logger.level, LogLevel.INFO)

if __name__ == '__main__':
    unittest.main()
