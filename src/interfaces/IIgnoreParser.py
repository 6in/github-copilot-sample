from abc import ABC, abstractmethod
from typing import List

class IIgnoreParser(ABC):
    @abstractmethod
    def parse(self, ignore_file_path: str) -> List[str]:
        """
        除外パターンファイル（例: .gitignore）を解析し、パターンリストを返す。
        :param ignore_file_path: 除外パターンファイルのパス
        :return: 除外パターンのリスト
        """
        pass
