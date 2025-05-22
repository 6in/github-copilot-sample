import unittest
import sys
from unittest.mock import patch
from src.main import parse_arguments

class TestMain(unittest.TestCase):
    
    def test_parse_arguments(self):
        """引数解析のテスト"""
        test_args = ['main.py', 'test_pattern', '/test/dir', '-e', 'py,txt', '-v']
        
        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            
            self.assertEqual(args.pattern, 'test_pattern')
            self.assertEqual(args.directory, '/test/dir')
            self.assertEqual(args.extensions, ['py,txt'])
            self.assertTrue(args.verbose)
            self.assertEqual(args.ignore_file, '.gitignore')
            self.assertFalse(args.no_ignore)

if __name__ == '__main__':
    unittest.main()
