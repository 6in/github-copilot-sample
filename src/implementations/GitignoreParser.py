import os
from typing import List, Optional
import pathspec
from src.interfaces.IIgnoreParser import IIgnoreParser

class GitignoreParser(IIgnoreParser):
    """
    IIgnoreParserの実装クラス。.gitignoreファイルを解析し、除外パターンのリストを返す。
    pathspecライブラリを使用して、gitignoreパターンの解析とマッチングを行う。
    """
    
    def __init__(self):
        """GitignoreParserの初期化"""
        self.spec = None
        
    def parse(self, ignore_file_path: str) -> List[str]:
        """
        除外パターンファイル（.gitignore）を解析し、パターンリストを返す。
        
        :param ignore_file_path: 除外パターンファイルのパス
        :return: 除外パターンのリスト
        :raises FileNotFoundError: ファイルが見つからない場合
        :raises IOError: ファイルの読み取りに失敗した場合
        """
        if not os.path.exists(ignore_file_path):
            raise FileNotFoundError(f"除外パターンファイルが見つかりません: {ignore_file_path}")
        
        try:
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                patterns = []
                for line in f:
                    line = line.strip()
                    # 空行やコメント行をスキップ
                    if not line or line.startswith('#'):
                        continue
                    patterns.append(line)
                
                # pathspecでパターンを解析
                self.spec = pathspec.PathSpec.from_lines(
                    pathspec.patterns.GitWildMatchPattern, patterns
                )
                
                return patterns
        except IOError as e:
            raise IOError(f"ファイルの読み取りに失敗しました: {ignore_file_path} - {str(e)}")
    
    def matches(self, path: str) -> bool:
        """
        指定されたパスが除外パターンにマッチするかを判定する。
        
        :param path: 判定するパス
        :return: パターンにマッチする場合はTrue、そうでなければFalse
        :raises ValueError: パターンが解析されていない場合
        """
        if self.spec is None:
            raise ValueError("除外パターンが解析されていません。先にparse()メソッドを呼び出してください。")
        
        return self.spec.match_file(path)
    
    def filter_paths(self, paths: List[str]) -> List[str]:
        """
        パスのリストから、除外パターンにマッチするものを除外する。
        
        :param paths: フィルタリングするパスのリスト
        :return: 除外パターンにマッチしないパスのリスト
        :raises ValueError: パターンが解析されていない場合
        """
        if self.spec is None:
            raise ValueError("除外パターンが解析されていません。先にparse()メソッドを呼び出してください。")
        
        return [path for path in paths if not self.matches(path)]
    
    @staticmethod
    def create_from_patterns(patterns: List[str]) -> 'GitignoreParser':
        """
        パターンリストから直接GitignoreParserインスタンスを作成する。
        
        :param patterns: 除外パターンのリスト
        :return: GitignoreParserインスタンス
        """
        parser = GitignoreParser()
        parser.spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, patterns
        )
        return parser
