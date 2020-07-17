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

    def test_validate_the_string_stream_key(self):
        ks = string_stream(" Name =Adewale Azeez,Project =konfiger, Date=April 24 2020", '=', ',')
        self.assertEqual(ks.next()[0], "Name")
        self.assertEqual(ks.next()[0], "Project")
        self.assertEqual(ks.next()[0], "Date")

    def test_validate_the_string_stream_value(self):
        ks = string_stream("Name=Adewale Azeez,Project=konfiger, Date=April 24 2020", '=', ',')
        self.assertEqual(ks.next()[1], "Adewale Azeez")
        self.assertEqual(ks.next()[1], "konfiger")
        self.assertEqual(ks.next()[1], "April 24 2020")

    def test_string_stream_key_trimming(self):
        ks = string_stream(" Name =Adewale Azeez:Project =konfiger: Date=April 24 2020", '=', ':')
        self.assertEqual(ks.is_trimming_key(), True)
        ks.set_trimming_key(False)
        with self.assertRaises(TypeError) as context:
            ks.set_trimming_key("Hello World")
        self.assertTrue('Invalid argument, expecting a bool found' in str(context.exception))
        self.assertEqual(ks.is_trimming_key(), False)
        self.assertEqual(ks.next()[0], " Name ")
        self.assertEqual(ks.next()[0], "Project ")
        self.assertEqual(ks.next()[0], " Date")

    def test_the_single_pair_commenting_in_string_stream(self):
        ks = string_stream("Name:Adewale Azeez,//Project:konfiger,Date:April 24 2020", ':', ',')
        while ks.has_next():
            self.assertNotEqual(ks.next()[0], "Project")
        with self.assertRaises(BufferError) as context:
            self.assertNotEqual(ks.next()[0], "Project")
        self.assertTrue('You cannot read beyound the stream length, always use hasNext() to verify the Stream still has an entry' in str(context.exception))

    def test_the_single_pair_commenting_in_file_stream_1(self):
        ks = file_stream("test/test.comment.inf")
        ks.set_comment_prefix("[")
        while ks.has_next():
            self.assertEqual(ks.next()[0].startswith("["), False)

    def test_the_single_pair_commenting_in_file_stream(self):
        ks = file_stream("test/test.txt", ':',  ',')
        while ks.has_next():
            self.assertEqual(ks.next()[0].startswith("//"), False)

    def test_string_stream_value_trimming(self):
        ks = string_stream(" Name =Adewale Azeez :Project = konfiger: Date= April 24 2020 :Language = Multiple Languages", '=', ':')
        self.assertNotEqual(ks.is_trimming_value(), False)
        with self.assertRaises(TypeError) as context:
            ks.set_trimming_value("Hello World")
        self.assertTrue('Invalid argument, expecting a bool found' in str(context.exception))
        self.assertEqual(ks.is_trimming_value(), True)
        self.assertEqual(ks.next()[1], "Adewale Azeez")
        self.assertEqual(ks.next()[1], "konfiger")
        self.assertEqual(ks.next()[1], "April 24 2020")
        self.assertEqual(ks.next()[1], "Multiple Languages")    
    
    def test_string_stream_key_value_trimming(self):
        entries_str = " Name =Adewale Azeez :Project = konfiger: Date= April 24 2020 :Language = Multiple Languages"
        ks = string_stream(entries_str, '=', ':')
        ks1 = string_stream(entries_str, '=', ':')
        self.assertEqual(ks.next()[0], "Name")
        self.assertEqual(ks.next()[0], "Project")
        self.assertEqual(ks.next()[0], "Date")
        self.assertEqual(ks.next()[0], "Language")
        
        
        self.assertEqual(ks1.next()[1], "Adewale Azeez")
        self.assertEqual(ks1.next()[1], "konfiger")
        self.assertEqual(ks1.next()[1], "April 24 2020")
        self.assertEqual(ks1.next()[1], "Multiple Languages")

    def read_multiline_entry_and_test_continuation_char_in_file_stream(self):
        print("TODO NOW")
            
    def read_multiline_entry_and_test_continuation_char_in_file_stream(self):
        print("TODO")

if __name__ == '__main__': 
    unittest.main() 
