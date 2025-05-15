from abc import ABC, abstractmethod
from typing import List, Tuple

class IFormatter(ABC):
    @abstractmethod
    def format(self, matches: List[Tuple[str, int, int, str]]) -> str:
        """
        検索結果を標準出力用に整形する。
        :param matches: (ファイルパス, 開始行, 終了行, 内容) のリスト
        :return: 整形済み文字列
        """
        pass
