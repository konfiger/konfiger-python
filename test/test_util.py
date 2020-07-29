#!python

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import escape_string, un_escape_string
  
class TestKonfigerUtil(unittest.TestCase): 
  
    def test_check_escape_and_unescape_seperator(self):         
        actual_str = "\\,Hello¬W\n-\t-\torld"
        t1 = escape_string(actual_str, '¬')
        t2 = un_escape_string(actual_str)
        
        self.assertNotEqual(actual_str, t1)
        self.assertEqual(t1, "\\,Hello^¬W\n-\t-\torld")
        self.assertNotEqual(t1, un_escape_string(t1, '¬'))
        self.assertNotEqual(actual_str, un_escape_string(t1))
        self.assertEqual(un_escape_string(t1, '¬'), actual_str)
        
        self.assertNotEqual(t1, t2)
        self.assertEqual(t2, "\\,Hello¬W\n-\t-\torld")
        self.assertNotEqual(t2, un_escape_string(t1))
        self.assertEqual(actual_str, un_escape_string(t2))
        self.assertEqual(un_escape_string(t1, '¬'), actual_str)
  
if __name__ == '__main__': 
    unittest.main() 
