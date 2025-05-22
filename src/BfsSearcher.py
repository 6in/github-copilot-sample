from pathlib import Path
from typing import List
from src.interfaces.ISearcher import ISearcher
from collections import deque

class BfsSearcher(ISearcher):
    def search(self, root_dir: Path, exts: List[str], ignore_patterns: List[str]) -> List[Path]:
        """
        ディレクトリ配下をBFSで探索し、条件に合致するファイルパスのリストを返す。
        :param root_dir: 探索開始ディレクトリ
        :param exts: 対象拡張子リスト（空なら全て）
        :param ignore_patterns: 除外パターンリスト
        :return: ファイルパスのリスト
        """
        result = []
        queue = deque([root_dir])
        while queue:
            current = queue.popleft()
            if any(current.match(pattern) for pattern in ignore_patterns):
                continue
            if current.is_dir():
                for child in current.iterdir():
                    queue.append(child)
            elif current.is_file():
                if not exts or current.suffix in exts:
                    result.append(current)
        return result
