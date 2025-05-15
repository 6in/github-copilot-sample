from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class ISearcher(ABC):
    @abstractmethod
    def search(self, root_dir: Path, exts: List[str], ignore_patterns: List[str]) -> List[Path]:
        """
        ディレクトリ配下を再帰的に探索し、条件に合致するファイルパスのリストを返す。
        :param root_dir: 探索開始ディレクトリ
        :param exts: 対象拡張子リスト（空なら全て）
        :param ignore_patterns: 除外パターンリスト
        :return: ファイルパスのリスト
        """
        pass
