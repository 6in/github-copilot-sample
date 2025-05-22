import re
from typing import List, Tuple
from src.interfaces.IMatcher import IMatcher

class RegexMatcher(IMatcher):
    def match(self, file_path: str, pattern: str) -> List[Tuple[int, int, str]]:
        """
        ファイル内で正規表現パターンにマッチする範囲を返す。
        :param file_path: 対象ファイルパス
        :param pattern: 正規表現パターン
        :return: (開始行, 終了行, マッチ内容) のリスト
        """
        results = []
        
        try:
            # UTF-8でファイルを読み込む
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 正規表現コンパイル（マルチラインモード）
            regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
            
            # 全マッチを検索
            for match in regex.finditer(content):
                # マッチした内容
                match_text = match.group(0)
                
                # マッチ開始位置から行番号を計算
                start_pos = match.start()
                end_pos = match.end() - 1 if match.end() > 0 else 0  # 終了位置は最後の文字のインデックス（空文字対策）
                
                # マッチ開始位置までの改行数をカウントして行番号を得る（0オリジン→1オリジン）
                start_line = content[:start_pos].count('\n') + 1
                
                # マッチ終了位置までの改行数をカウントして行番号を得る（0オリジン→1オリジン）
                end_line = content[:end_pos].count('\n') + 1
                
                results.append((start_line, end_line, match_text))
                
        except UnicodeDecodeError:
            # UTF-8以外のエンコーディングはスキップ
            pass
        except Exception as e:
            # その他のエラーは無視して継続（将来的にはロガーでログ出力）
            print(f"Error processing file {file_path}: {e}")
            pass
            
        return results
