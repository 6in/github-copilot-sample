from abc import ABC, abstractmethod
from typing import List, Tuple

class IMatcher(ABC):
    @abstractmethod
    def match(self, file_path: str, pattern: str) -> List[Tuple[int, int, str]]:
        """
        ファイル内で正規表現パターンにマッチする範囲を返す。
        :param file_path: 対象ファイルパス
        :param pattern: 正規表現パターン
        :return: (開始行, 終了行, マッチ内容) のリスト
        """
        pass
