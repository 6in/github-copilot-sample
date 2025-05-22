import sys
from datetime import datetime
from enum import Enum, auto
from src.interfaces.ILogger import ILogger

class LogLevel(Enum):
    """ログレベルを定義する列挙型"""
    ERROR = auto()
    INFO = auto()
    DEBUG = auto()

class SimpleLogger(ILogger):
    """
    ILoggerの標準実装。コンソールにログを出力する。
    
    ログの出力形式：
    [LEVEL] [yyyy-mm-dd HH:MM:SS] メッセージ
    
    例：
    [INFO] [2025-05-22 14:30:45] 処理を開始しました
    [ERROR] [2025-05-22 14:31:10] ファイルが見つかりません: /path/to/file.txt
    
    ログレベルに応じて出力の制御が可能。指定されたログレベル以下のメッセージのみ出力される。
    ERROR < INFO < DEBUG の順で詳細度が上がる。
    """
    
    def __init__(self, level: LogLevel = LogLevel.INFO, output_enabled: bool = True, log_level: str = None):
        """
        SimpleLoggerを初期化する。
        
        :param level: ログレベル（デフォルトはINFO）
        :param output_enabled: 標準出力への出力を有効にするかどうか（デフォルトはTrue）
        :param log_level: 文字列で指定するログレベル（"DEBUG", "INFO", "ERROR"）
        """
        self.output_enabled = output_enabled
        self.log_history = []  # テスト用にログ履歴を保持
        
        # 文字列でログレベルが指定されている場合はそれを優先
        if log_level is not None:
            if log_level.upper() == "DEBUG":
                self.level = LogLevel.DEBUG
            elif log_level.upper() == "INFO":
                self.level = LogLevel.INFO
            elif log_level.upper() == "ERROR":
                self.level = LogLevel.ERROR
            else:
                # 不明なレベルの場合はINFOにフォールバック
                self.level = LogLevel.INFO
        else:
            self.level = level
        
    def set_level(self, level: LogLevel):
        """
        ログレベルを設定する。
        
        :param level: 新しいログレベル
        """
        self.level = level
        
    def info(self, msg: str):
        """
        INFOレベルのログを出力する。
        
        :param msg: ログメッセージ
        """
        if self.level.value >= LogLevel.INFO.value:
            log_line = self._log("INFO", msg)
            return log_line
        return None
            
    def debug(self, msg: str):
        """
        DEBUGレベルのログを出力する。
        
        :param msg: ログメッセージ
        """
        if self.level.value >= LogLevel.DEBUG.value:
            log_line = self._log("DEBUG", msg)
            return log_line
        return None
            
    def error(self, msg: str):
        """
        ERRORレベルのログを出力する。
        
        :param msg: ログメッセージ
        """
        # ERRORは常に出力する
        log_line = self._log("ERROR", msg, file=sys.stderr)
        return log_line
            
    def _log(self, level_str: str, msg: str, file=sys.stdout):
        """
        ログを整形して出力する内部メソッド。
        
        :param level_str: ログレベルの文字列表現
        :param msg: ログメッセージ
        :param file: 出力先（デフォルトは標準出力、エラーの場合は標準エラー出力）
        :return: 整形されたログ行
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{level_str}] [{timestamp}] {msg}"
        
        # ログ履歴に追加
        self.log_history.append(log_line)
        
        # 出力が有効な場合のみ標準出力/エラー出力に書き込む
        if self.output_enabled:
            print(log_line, file=file)
            
        return log_line
        
    def get_logs(self, level: str = None):
        """
        記録されたログを取得する。テスト用のメソッド。
        
        :param level: フィルタリングするログレベル（省略可）
        :return: 指定されたレベルのログのリスト
        """
        if level is None:
            return self.log_history
        
        return [log for log in self.log_history if f"[{level}]" in log]
