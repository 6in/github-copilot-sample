import unittest
from src.factories.ModuleFactory import ModuleFactory
from src.interfaces.ISearcher import ISearcher
from src.interfaces.IMatcher import IMatcher
from src.interfaces.IFormatter import IFormatter
from src.interfaces.ILogger import ILogger
from src.interfaces.IIgnoreParser import IIgnoreParser
from src.implementations.BfsSearcher import BfsSearcher
from src.implementations.RegexMatcher import RegexMatcher
from src.implementations.SimpleFormatter import SimpleFormatter
from src.implementations.SimpleLogger import SimpleLogger
from src.implementations.GitignoreParser import GitignoreParser

class TestModuleFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ModuleFactory()
    
    def test_create_searcher(self):
        """Searcherの生成テスト"""
        searcher = self.factory.create_searcher()
        self.assertIsInstance(searcher, ISearcher)
        self.assertIsInstance(searcher, BfsSearcher)
        
        with self.assertRaises(ValueError):
            self.factory.create_searcher('invalid_type')
    
    def test_create_matcher(self):
        """Matcherの生成テスト"""
        matcher = self.factory.create_matcher()
        self.assertIsInstance(matcher, IMatcher)
        self.assertIsInstance(matcher, RegexMatcher)
        
        with self.assertRaises(ValueError):
            self.factory.create_matcher('invalid_type')
    
    def test_create_formatter(self):
        """Formatterの生成テスト"""
        formatter = self.factory.create_formatter()
        self.assertIsInstance(formatter, IFormatter)
        self.assertIsInstance(formatter, SimpleFormatter)
        
        with self.assertRaises(ValueError):
            self.factory.create_formatter('invalid_type')
    
    def test_create_logger(self):
        """Loggerの生成テスト"""
        logger = self.factory.create_logger()
        self.assertIsInstance(logger, ILogger)
        self.assertIsInstance(logger, SimpleLogger)
        
        with self.assertRaises(ValueError):
            self.factory.create_logger('invalid_type')
    
    def test_create_ignore_parser(self):
        """IgnoreParserの生成テスト"""
        parser = self.factory.create_ignore_parser()
        self.assertIsInstance(parser, IIgnoreParser)
        self.assertIsInstance(parser, GitignoreParser)
        
        with self.assertRaises(ValueError):
            self.factory.create_ignore_parser('invalid_type')
    
    def test_with_config(self):
        """設定付きの初期化テスト"""
        config = {
            'default_searcher': 'bfs',
            'default_matcher': 'regex',
            'log_level': 'DEBUG'
        }
        factory = ModuleFactory(config)
        self.assertEqual(factory.config, config)
        
        # 設定があっても正しいインスタンスが生成されることを確認
        searcher = factory.create_searcher()
        self.assertIsInstance(searcher, BfsSearcher)

if __name__ == "__main__":
    unittest.main()
