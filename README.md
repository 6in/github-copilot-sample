# CLI検索ツール

## 概要
このプロジェクトは、コマンドラインからディレクトリを再帰的に探索し、正規表現パターンにマッチするファイルの内容を検索するCLIツールです。インターフェースベース＋Factoryパターンを採用した拡張性の高い設計となっています。

## 特徴
- 再帰的なディレクトリ探索（BFS: 幅優先探索）
- 正規表現を使用したファイル内容の検索
- 拡張子指定による検索対象の絞り込み
- `.gitignore`形式の除外パターン対応
- ログレベル制御（DEBUG、INFO、ERROR）
- 検索結果の整形出力

## インストール方法

### 開発環境のセットアップ
```bash
# 仮想環境の作成と有効化（任意）
python -m venv .venv
source .venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt

# パッケージを開発モードでインストール
pip install -e .
```

## 使用方法

### 基本的な使い方
```bash
# パッケージをインストールした場合
cli-search "検索パターン" [検索ディレクトリ]

# または直接スクリプトを実行する場合
python src/main.py "検索パターン" [検索ディレクトリ]
```

### オプション
- `-e, --extensions`: 検索対象の拡張子（例: `py,js,txt`）
- `-i, --ignore-file`: 除外パターンを含むファイル（デフォルト: `.gitignore`）
- `--no-ignore`: 除外パターンを無視する
- `-v, --verbose`: 詳細なログを出力する

### 使用例
```bash
# カレントディレクトリ内の全ファイルから"function"を検索
python src/main.py "function"

# 指定ディレクトリ内のPythonファイルから"class"を検索
python src/main.py "class" /path/to/dir -e py

# 詳細ログ出力とカスタム除外ファイル指定
python src/main.py "import" /path/to/dir -v -i .customignore

# 除外パターンを無視してすべてのファイルを検索対象に
python src/main.py "test" /path/to/dir --no-ignore
```

## アーキテクチャ

### 設計パターン
- **インターフェースベース設計**: 各機能をインターフェース（抽象基底クラス）で定義
- **Factoryパターン**: 設定や引数に応じて適切な実装クラスをインスタンス化
- **依存性注入**: 各コンポーネント間の疎結合を実現

### 主要コンポーネント
- **ISearcher**: ファイル探索インターフェース（実装: BfsSearcher）
- **IMatcher**: パターンマッチングインターフェース（実装: RegexMatcher）
- **IFormatter**: 結果整形インターフェース（実装: SimpleFormatter）
- **ILogger**: ログ出力インターフェース（実装: SimpleLogger）
- **IIgnoreParser**: 除外パターン解析インターフェース（実装: GitignoreParser）
- **ModuleFactory**: 各インターフェースの実装を生成するファクトリークラス

## 開発環境
- Python 3.9+
- 依存ライブラリ:
  - pathspec (GitignoreParserで使用)

### セットアップ
```bash
# 仮想環境の作成と有効化（推奨）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# または
.venv\Scripts\activate  # Windows

# 依存ライブラリのインストール
pip install -r requirements.txt
```

### テスト実行
```bash
# すべてのテストを実行
python -m unittest discover tests

# 特定のテストを実行
python -m unittest tests/test_regex_matcher.py
```

## 今後の開発予定
- エラー処理の強化
- 出力フォーマットのカスタマイズオプション
- 詳細表示モードの実装
- 大規模ディレクトリでの探索速度改善
- サードパーティライブラリ（rich/tqdm等）対応

## ライセンス
このプロジェクトはMITライセンスの下で提供されています。
