#!python {0}

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import from_file, from_string

class TestKonfiger(unittest.TestCase): 

    def test_validate_kon_string_stream_entries(self):
        kon = from_string("""
String=This is a string
Number=215415245
Float=56556.436746
Boolean=true
""", False)

        self.assertEqual(kon.get("String"), "This is a string")
        self.assertEqual(kon.get("Number"), "215415245")
        self.assertEqual(kon.get("Float"), "56556.436746")
        self.assertNotEqual(kon.get("Number"), "true")
        self.assertEqual(kon.get("Boolean"), "true")
        kon.put("String", "This is an updated string")
        self.assertEqual(kon.get("String"), "This is an updated string")

    def test_validate_kon_entries_get_method(self):
        kon = from_file('test/test.config.ini')
        kon.put("One", kon)
        kon.put("Two", '"hello", "world"')
        kon.put("Three", 3)
        kon.put_int("Four", 4)
        kon.put_boolean("Five", True)
        kon.put("Six", False)
        kon.put("Seven", "121251656.1367367263726")
        kon.put_float("Eight", 0.21)
        
        self.assertNotEqual(kon.get("One"), str(kon))
        self.assertEqual(kon.get("Two"), '"hello", "world"')
        self.assertEqual(int(kon.get("Three")), 3)
        self.assertEqual(int(kon.get("Four")), 4)
        self.assertEqual(kon.get("Five"), "True")
        self.assertEqual(kon.get("Six"), "False")
        self.assertEqual(kon.get("Seven"), "121251656.1367367263726")
        self.assertEqual(kon.get("Eight"), "0.21")

    def test_validate_lazyload_kon_entries_get_with_fallback(self):
        kon = from_file('test/test.config.ini', True)
        
        self.assertEqual(kon.get("Occupation", "Pen Tester"), "Software Engineer") 
        self.assertEqual(kon.get("Hobby", "Worm Creation"), "i don't know")
        self.assertEqual(kon.get("Fav OS"), None)
        self.assertNotEqual(kon.get("Fav OS", "Whatever get work done"), None)

    def test_validate_kon_get_returned_types(self):
        kon = from_string('')
        kon.put("One", kon)
        kon.put_long("Two", 123456789)
        kon.put_boolean("Bool", True)
        kon.put_float("Float", 123.56)
        kon.put_string("Dummy", "Noooooo 1")
        kon.put_string("Dummy2", "Noooooo 2")

        self.assertEqual(kon.get("Two"), "123456789")
        self.assertEqual(kon.get_long("Two"), 123456789)
        self.assertNotEqual(kon.get_long("Two"), "123456789")

        self.assertEqual(kon.get("Bool"), "True")
        self.assertEqual(kon.get_boolean("Two"), False)
        self.assertNotEqual(kon.get_boolean("Two"), True)
        self.assertNotEqual(kon.get_boolean("Two"), "True")

        self.assertEqual(kon.get("Float"), "123.56")
        self.assertEqual(kon.get_float("Float"), 123.56)
        self.assertNotEqual(kon.get_float("Float"), "123.56") 
        

if __name__ == '__main__': 
    unittest.main() 