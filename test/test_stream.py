#!python

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import file_stream, string_stream
  
class TestKonfigerStream(unittest.TestCase): 

    def test_should_throw_exceptions(self):
        self.assertRaises(TypeError, file_stream)
        
        with self.assertRaises(TypeError) as context:
            ks = file_stream(20)
        self.assertTrue('Invalid argument expecting str found' in str(context.exception))
        
        with self.assertRaises(FileNotFoundError) as context:
            ks = file_stream("./tryer.ini")
        self.assertTrue('file does not exists' in str(context.exception))
        
        with self.assertRaises(TypeError) as context:
            ks = file_stream("./setup.py", ',', "==")
        self.assertTrue('Invalid argument for seperator expecting char' in str(context.exception))
        
        with self.assertRaises(TypeError) as context:
            ks = string_stream(30)
        self.assertTrue('Invalid argument expecting str found' in str(context.exception))

    def test_should_successfully_initialize(self):
        self.assertNotEqual(file_stream("./setup.py"), None)

    def test_validate_the_file_stream_value(self):
        ks = file_stream("test/test.config.ini", '=', '\n')
        while ks.has_next():
            self.assertNotEqual(ks.next(), None)
  
if __name__ == '__main__': 
    unittest.main() 
