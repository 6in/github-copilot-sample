#!/usr/bin/env python3
"""
CLI検索ツール: コマンドラインからディレクトリを再帰的に探索し、
パターンにマッチするファイルの内容を検索するツール
"""
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

from src.factories.ModuleFactory import ModuleFactory

# エクスポートする関数の明示的指定
__all__ = ['parse_arguments', 'create_config', 'main']

def parse_arguments() -> argparse.Namespace:
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(
        description='ファイル内容の検索ツール',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'pattern',
        help='検索する正規表現パターン'
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='検索を開始するディレクトリ（デフォルト: カレントディレクトリ）'
    )
    
    parser.add_argument(
        '-e', '--extensions',
        nargs='*',
        help='検索対象の拡張子（カンマ区切り、例: py,js,txt）'
    )
    
    parser.add_argument(
        '-i', '--ignore-file',
        default='.gitignore',
        help='除外パターンを含むファイル（デフォルト: .gitignore）'
    )
    
    parser.add_argument(
        '--no-ignore',
        action='store_true',
        help='除外パターンを無視する'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='詳細なログを出力する'
    )
    
    return parser.parse_args()

def create_config(args: argparse.Namespace) -> Dict[str, Any]:
    """引数から設定辞書を作成する"""
    config = {
        'pattern': args.pattern,
        'directory': args.directory,
        'verbose': args.verbose,
        'no_ignore': args.no_ignore,
        'ignore_file': args.ignore_file
    }
    
    # 拡張子処理
    if args.extensions:
        # 複数拡張子が渡された場合の処理
        exts = []
        for ext_group in args.extensions:
            # カンマで区切られた拡張子を分割
            exts.extend([ext.strip() for ext in ext_group.split(',') if ext.strip()])
        
        # 拡張子の先頭にドットがない場合は追加
        config['extensions'] = [ext if ext.startswith('.') else f'.{ext}' for ext in exts]
    else:
        config['extensions'] = []
    
    return config

def main():
    """メイン処理"""
    args = parse_arguments()
    config = create_config(args)
    
    # Factoryを使用して各コンポーネントを作成
    factory = ModuleFactory(config)
    
    # ロガーの作成
    log_level = 'DEBUG' if config['verbose'] else 'INFO'
    logger = factory.create_logger(logger_type='simple', log_level=log_level)
    logger.info(f"検索開始: パターン '{config['pattern']}' をディレクトリ '{config['directory']}' で検索します")
    
    try:
        # 除外パターンの解析
        ignore_patterns = []
        if not config['no_ignore']:
            ignore_parser = factory.create_ignore_parser()
            ignore_file_path = Path(config['directory']) / config['ignore_file']
            
            if ignore_file_path.exists():
                logger.debug(f"除外パターンファイルを解析: {ignore_file_path}")
                ignore_patterns = ignore_parser.parse(str(ignore_file_path))
                logger.debug(f"{len(ignore_patterns)}個の除外パターンを読み込みました")
            else:
                logger.debug(f"除外パターンファイルが見つかりません: {ignore_file_path}")
        
        # ファイル検索
        searcher = factory.create_searcher()
        logger.debug(f"ファイル検索開始: ディレクトリ={config['directory']}, 拡張子={config['extensions']}")
        files = searcher.search(
            root_dir=Path(config['directory']),
            exts=config['extensions'],
            ignore_patterns=ignore_patterns
        )
        logger.debug(f"{len(files)}個のファイルが見つかりました")
        
        # パターンマッチング
        matcher = factory.create_matcher()
        all_matches = []
        
        for file_path in files:
            logger.debug(f"ファイル内検索: {file_path}")
            try:
                matches = matcher.match(str(file_path), config['pattern'])
                if matches:
                    all_matches.extend([(str(file_path), start, end, content) for start, end, content in matches])
            except Exception as e:
                logger.error(f"ファイル '{file_path}' の検索中にエラーが発生: {str(e)}")
        
        # 結果の整形と表示
        formatter = factory.create_formatter()
        formatted_output = formatter.format(all_matches)
        
        if all_matches:
            logger.info(f"{len(all_matches)}個のマッチが見つかりました")
            print(formatted_output)
        else:
            logger.info("マッチするものが見つかりませんでした")
        
        return 0
    
    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
