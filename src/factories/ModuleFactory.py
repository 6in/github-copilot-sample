from typing import Dict, Type, Any, Optional

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

class ModuleFactory:
    """
    設定や引数に応じて、各インターフェースの実装を生成するファクトリークラス。
    インターフェースベースの依存性注入を実現し、コンポーネント間の疎結合を維持する。
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        ファクトリークラスの初期化。
        
        :param config: 設定情報の辞書（オプション）
        """
        self.config = config or {}
        
        # 各インターフェースの実装マッピング
        self.searcher_implementations: Dict[str, Type[ISearcher]] = {
            'bfs': BfsSearcher
        }
        
        self.matcher_implementations: Dict[str, Type[IMatcher]] = {
            'regex': RegexMatcher
        }
        
        self.formatter_implementations: Dict[str, Type[IFormatter]] = {
            'simple': SimpleFormatter
        }
        
        self.logger_implementations: Dict[str, Type[ILogger]] = {
            'simple': SimpleLogger
        }
        
        self.ignore_parser_implementations: Dict[str, Type[IIgnoreParser]] = {
            'gitignore': GitignoreParser
        }
    
    def create_searcher(self, searcher_type: str = 'bfs', **kwargs) -> ISearcher:
        """
        ISearcher実装のインスタンスを生成する。
        
        :param searcher_type: 使用するSearcherの種類
        :param kwargs: Searcher初期化時の追加パラメータ
        :return: ISearcherインスタンス
        :raises ValueError: 指定されたタイプの実装が存在しない場合
        """
        if searcher_type not in self.searcher_implementations:
            raise ValueError(f"サポートされていないSearcherタイプです: {searcher_type}")
        
        searcher_class = self.searcher_implementations[searcher_type]
        return searcher_class(**kwargs)
    
    def create_matcher(self, matcher_type: str = 'regex', **kwargs) -> IMatcher:
        """
        IMatcher実装のインスタンスを生成する。
        
        :param matcher_type: 使用するMatcherの種類
        :param kwargs: Matcher初期化時の追加パラメータ
        :return: IMatcherインスタンス
        :raises ValueError: 指定されたタイプの実装が存在しない場合
        """
        if matcher_type not in self.matcher_implementations:
            raise ValueError(f"サポートされていないMatcherタイプです: {matcher_type}")
        
        matcher_class = self.matcher_implementations[matcher_type]
        return matcher_class(**kwargs)
    
    def create_formatter(self, formatter_type: str = 'simple', **kwargs) -> IFormatter:
        """
        IFormatter実装のインスタンスを生成する。
        
        :param formatter_type: 使用するFormatterの種類
        :param kwargs: Formatter初期化時の追加パラメータ
        :return: IFormatterインスタンス
        :raises ValueError: 指定されたタイプの実装が存在しない場合
        """
        if formatter_type not in self.formatter_implementations:
            raise ValueError(f"サポートされていないFormatterタイプです: {formatter_type}")
        
        formatter_class = self.formatter_implementations[formatter_type]
        return formatter_class(**kwargs)
    
    def create_logger(self, logger_type: str = 'simple', **kwargs) -> ILogger:
        """
        ILogger実装のインスタンスを生成する。
        
        :param logger_type: 使用するLoggerの種類
        :param kwargs: Logger初期化時の追加パラメータ
        :return: ILoggerインスタンス
        :raises ValueError: 指定されたタイプの実装が存在しない場合
        """
        if logger_type not in self.logger_implementations:
            raise ValueError(f"サポートされていないLoggerタイプです: {logger_type}")
        
        logger_class = self.logger_implementations[logger_type]
        return logger_class(**kwargs)
    
    def create_ignore_parser(self, parser_type: str = 'gitignore', **kwargs) -> IIgnoreParser:
        """
        IIgnoreParser実装のインスタンスを生成する。
        
        :param parser_type: 使用するIgnoreParserの種類
        :param kwargs: IgnoreParser初期化時の追加パラメータ
        :return: IIgnoreParserインスタンス
        :raises ValueError: 指定されたタイプの実装が存在しない場合
        """
        if parser_type not in self.ignore_parser_implementations:
            raise ValueError(f"サポートされていないIgnoreParserタイプです: {parser_type}")
        
        parser_class = self.ignore_parser_implementations[parser_type]
        return parser_class(**kwargs)
