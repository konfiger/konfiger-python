#!python {0}

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import from_file, from_string

class TestKonfiger(unittest.TestCase): 

    def test_validate_konfiger_string_stream_entries(self):
        kon = from_string("""
String=This is a string
Number=215415245
Float=56556.436746
Boolean=true
""", True)
        self.assertEqual(kon.get("String"), "This is a string")
        

if __name__ == '__main__': 
    unittest.main() 