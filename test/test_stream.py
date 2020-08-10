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
        self.assertTrue('You cannot read beyound the stream length, always use has_next() to verify the Stream still has an entry' in str(context.exception))

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

    def test_read_multiline_entry_and_test_continuation_char_in_file_stream(self):
        ks = file_stream("test/test.contd.conf")
        while ks.has_next():
            self.assertEqual(ks.next()[1].endswith('\\'), False)
            
    def test_read_multiline_entry_and_test_continuation_char_in_string_stream(self):
        ks = string_stream("""
Description = This project is the closest thing to Android +
              [Shared Preference](https://developer.android.com/reference/android/content/SharedPreferences) +
              in other languages and off the Android platform.
ProjectName = konfiger
ProgrammingLanguages = C, C++, C#, Dart, Elixr, Erlang, Go, +
                        Haskell, Java, Kotlin, NodeJS, Powershell, +
                        Python, Ring, Rust, Scala, Visual Basic, +
                        and whatever language possible in the future
        """)
        ks.set_continuation_char('+')
        while ks.has_next():
            self.assertEqual(ks.next()[1].endswith('\\'), False)
            
    def test_backward_slash_ending_value(self):
        ks = string_stream("uri1 = http://uri1.thecarisma.com/core/api/v1/\r\n" +
                "uri2 = http://uri2.thecarisma.com/core/api/v2/\r\n" +
                "ussd.uri = https://ussd.thecarisma.com/")
        count = 0
        while ks.has_next():
            self.assertEqual(ks.next()[1].endswith("/"), True)
            count += 1
        self.assertEqual(count, 3)
        
    def test_escape_slash_ending(self):
        ks = string_stream("external-resource-location = \\\\988.43.13.9\\testing\\public\\sansportal\\rideon\\\\\r\n" +
                "boarding-link = https://boarding.thecarisma.com/konfiger\r\n" +
                "ussd.uri = thecarisma.com\\")
        count = 0
        while ks.has_next():
            self.assertNotEqual(len(ks.next()[1]), 0)
            count += 1
        self.assertEqual(count, 3)
        
    def test_error_tolerancy_in_string_stream(self):
        ks = string_stream("Firt=1st", '-', '$', True)
        
        self.assertEqual(ks.is_error_tolerant(), True)
        while ks.has_next():
            self.assertEqual(len(ks.next()[1]), 0)
        
    def test_error_tolerancy_in_file_stream(self):
        ks = file_stream("test/test.comment.inf")
        
        self.assertEqual(ks.is_error_tolerant(), False)
        while ks.has_next():
            with self.assertRaises(LookupError) as context:
                self.assertEqual(len(ks.next()[1]), 0)
            self.assertTrue('Invalid entry detected near Line' in str(context.exception))
            break
        
        ks.error_tolerance(True)
        self.assertEqual(ks.is_error_tolerant(), True)
        while ks.has_next():
            self.assertNotEqual(ks.next()[1], None)

if __name__ == '__main__': 
    unittest.main() 
