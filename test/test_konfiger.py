#!python

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import from_file, from_string, from_stream, file_stream, string_stream

class TestKonfiger(unittest.TestCase): 

    def test_validate_kon_string_stream_entries(self):
        kon = from_string("""
String=This is a string
Number=215415245
Float=56556.436746
Boolean=True
""", False)

        self.assertEqual(kon.get("String"), "This is a string")
        self.assertEqual(kon.get("Number"), "215415245")
        self.assertEqual(kon.get("Float"), "56556.436746")
        self.assertNotEqual(kon.get("Number"), "True")
        self.assertEqual(kon.get("Boolean"), "True")
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

    def test_validate_konfiger_default_value_for_non_existing_key(self):
        kon = from_string('')
        
        self.assertEqual(kon.get("Name"), None)
        self.assertNotEqual(kon.get_string("Name"), None)
        self.assertEqual(kon.get_string("Name"), "")
        self.assertNotEqual(kon.get("Name", "Adewale Azeez"), None)
        self.assertEqual(kon.get("Name", "Adewale Azeez"), "Adewale Azeez")
        self.assertEqual(kon.get_boolean("CleanupOnClose"), False)
        self.assertNotEqual(kon.get_boolean("CleanupOnClose", True), False)
        self.assertEqual(kon.get_long("TheNumber"), 0)
        self.assertEqual(kon.get_long("TheNumber", 123), 123)
        self.assertEqual(kon.get_float("TheNumber"), 0.0)
        self.assertNotEqual(kon.get_float("TheNumber"), 0.1)

    def test_remove_entry_and_validate_size(self):
        kon = from_string('One=111,Two=222,Three=333', False, '=', ',')
        kon.stream.error_tolerance(True)
    
        self.assertEqual(len(kon), 3)
        self.assertNotEqual(kon.get("Two"), None)
        self.assertEqual(kon.remove("Two"), "222")
        self.assertEqual(kon.get("Two"), None)
        self.assertEqual(len(kon), 2)
        self.assertEqual(kon.remove(0), "111")
        self.assertEqual(len(kon), 1)
        self.assertEqual(kon.get("Three"), "333")

    def test_set_get_delimeter_and_seperator(self):
        kon = from_file('test/test.config.ini', True)
        
        self.assertEqual(kon.get_seperator(), "\n")
        self.assertEqual(kon.get_delimeter(), "=")
        self.assertEqual(len(str(kon).split("\n")) > 2, True)
        kon.set_seperator('-')
        kon.set_delimeter('+')
        self.assertEqual(kon.get_seperator(), "-")
        self.assertEqual(kon.get_delimeter(), "+")
        self.assertEqual(len(str(kon).split("\n")), 1)

    def test_escaping_and_unescaping_entries_and_save(self):
        ks = file_stream('test/test.config.ini')
        ks1 = file_stream('test/test.txt', ':',  ',')
        kon = from_stream(ks)
        kon1 = from_stream(ks1)
        
        self.assertEqual(kon.get("Hobby"), "i don't know")
        self.assertEqual(kon1.get("Hobby"), kon.get("Hobby"))
        self.assertEqual(kon1.get("Hobby"), "i don't know")
        kon.save('test/test.config.ini')
        
        new_ks = file_stream('test/test.config.ini')
        new_kon = from_stream(new_ks, True)
        new_kon1 = from_file('test/test.txt', True, ':',  ',')
        self.assertEqual(str(kon), str(kon))
        self.assertEqual(str(kon1), str(kon1))

    def test_complex_and_confusing_seperator(self):
        kon = from_string('Occupation=Software En^gineergLocation=Ni^geriagState=La^gos', False, '=', 'g')
        
        self.assertEqual(len(kon), 3)
        self.assertEqual(str(kon).find("^g") > -1, True)
        for key, value in kon.entries():
            self.assertEqual(value.find("^g") > -1, False)
        kon.set_seperator('f')
        self.assertEqual(kon.get("Occupation"), "Software Engineer")
        kon.set_seperator('\n')
        self.assertEqual(str(kon).find("^g") > -1, False)
        self.assertEqual(len(kon), 3)
        for key, value in kon.entries():
            self.assertEqual(value.find("\\g") > -1, False)

    def test_append_new_unparsed_entries_from_string_and_file(self):
        kon = from_string('')
        
        self.assertEqual(len(kon), 0)    
        kon.append_string('Language=English')
        self.assertEqual(len(kon), 1)
        self.assertEqual(kon.get("Name"), None)
        self.assertNotEqual(kon.get("Name"), "Adewale Azeez")
        self.assertEqual(kon.get("Language"), "English")
        
        kon.append_file('test/test.config.ini')
        self.assertNotEqual(kon.get("Name"), None)
        self.assertEqual(kon.get("Name"), "Adewale Azeez")

    def test_prev_and_current_cache(self):
        kon = from_string('')
        
        kon.put("Name", "Adewale")
        kon.put("Project", "konfiger")
        kon.put_int("Year", 2020)
        
        self.assertEqual(kon.get_int("Year"), 2020)
        self.assertEqual(kon.get("Project"), "konfiger")
        self.assertEqual(kon.get("Name"), "Adewale")
        self.assertEqual(kon.get_int("Year"), 2020)
        self.assertEqual(kon.current_cache_object["ckey"], "Name")
        self.assertEqual(kon.prev_cache_object["ckey"], "Year")
        self.assertEqual(kon.current_cache_object["cvalue"], "Adewale")
        self.assertEqual(kon.prev_cache_object["cvalue"], "2020")
        self.assertEqual(kon.get("Name"), "Adewale")
        self.assertEqual(kon.get("Name"), "Adewale")
        self.assertEqual(kon.get("Project"), "konfiger")
        self.assertEqual(kon.get("Name"), "Adewale")
        self.assertEqual(kon.get("Name"), "Adewale")
        self.assertEqual(kon.get("Name"), "Adewale")
        self.assertEqual(kon.current_cache_object["ckey"], "Project")
        self.assertEqual(kon.prev_cache_object["ckey"], "Name")
        self.assertEqual(kon.current_cache_object["cvalue"], "konfiger")
        self.assertEqual(kon.prev_cache_object["cvalue"], "Adewale")

    def test_the_single_pair_commenting_in_string_stream_konfiger(self):
        ks = string_stream('Name:Adewale Azeez,//Project:konfiger,Date:April 24 2020', ':', ',')
        kon = from_stream(ks)
        
        for key, value in kon.entries():
            self.assertNotEqual([key, value], "Project")
        self.assertEqual(len(kon), 2)

    def test_contains_with_lazy_load(self):
        ks = file_stream('test/test.comment.inf')
        ks.set_comment_prefix("[")
        kon = from_stream(ks)
        
        self.assertEqual(kon.contains("File"), True)
        self.assertEqual(kon.contains("Project"), True)
        self.assertEqual(kon.contains("Author"), True)

    def test_read_multiline_entry_from_file_stream(self):
        ks = file_stream('test/test.contd.conf')
        kon = from_stream(ks)
        
        self.assertEqual(kon.get("ProgrammingLanguages").find("Kotlin, NodeJS, Powershell, Python, Ring, Rust") > 0, True)
        self.assertEqual(kon.get("ProjectName"), "konfiger")
        self.assertNotEqual(kon.get("Description").endswith(" in other languages and off the Android platform."), False)

    def test_check_size_in_lazyLoad_and_no_lazyLoad(self):
        ks = file_stream('test/test.contd.conf')
        kon = from_stream(ks, False)
        ks1 = file_stream('test/test.contd.conf')
        kon1 = from_stream(ks1, True)
        
        self.assertEqual(len(kon) > 0, True)
        self.assertEqual(len(kon1) > 0, True)
        self.assertEqual(kon.is_empty(), False)
        self.assertEqual(kon1.is_empty(), False)
        self.assertEqual(len(kon1), len(kon1))

    def test_check_put_comment_in_the_konfiger_object(self):
        kon = from_string('Name:Adewale Azeez,//Project:konfiger,Date:April 24 2020', False, ':', ',')
        kon.put_comment("A comment at the end")
        
        self.assertEqual(str(kon).find("//:A comment") > -1, True)

    def test_validate_konfiger_entries_with_case_sensitivity(self):
        kon = from_string("""
String=This is a string
Number=215415245
""", False)
    
        kon.set_case_sensitivity(True)
        self.assertEqual(kon.is_case_sensitive(), True)
        # with self.assertRaises(FileNotFoundError) as context:
            # self.assertEqual(kon.get("STRING"), "This is a string")
        # self.assertTrue('file does not exists' in str(context.exception))
        # with self.assertRaises(FileNotFoundError) as context:
            # self.assertEqual(kon.get("NUMBER"), "215415245")
        # self.assertTrue('file does not exists' in str(context.exception))
        
        kon.set_case_sensitivity(False)
        self.assertEqual(kon.is_case_sensitive(), False)
        self.assertEqual(kon.get("STRING"), "This is a string")
        self.assertEqual(kon.get("NUMBER"), "215415245")
        
        self.assertEqual(kon.get("strING"), "This is a string")
        self.assertEqual(kon.get("nuMBer"), "215415245")
        
        self.assertEqual(kon.get("STRiNg"), "This is a string")
        self.assertEqual(kon.get("nUMbeR"), "215415245")
        
        self.assertEqual(kon.get("string"), "This is a string")
        self.assertEqual(kon.get("number"), "215415245")

    def test_check_the_update_at_method(self):
        kon = from_string("Name:Adewale Azeez,//Project:konfiger,Date:April 24 2020", False, ':', ',')
        
        self.assertEqual(kon.get("Date"), "April 24 2020")
        self.assertEqual(kon.get("Name"), "Adewale Azeez")
        kon.update_at(1, "12 BC")
        kon.update_at(0, "Thecarisma")
        self.assertEqual(kon.get("Date"), "12 BC")
        self.assertEqual(kon.get("Name"), "Thecarisma")

    def test_save_content_and_validate_saved_content(self):
        kon = from_string("Name=Adewale Azeez,Date=April 24 2020,One=111,Two=222,Three=333", False, '=', ',')
        
        self.assertEqual(len(kon), 5)
        kon.save('test/konfiger.conf')
        kon2 = from_file('test/konfiger.conf', False, '=', ',')
        self.assertEqual(str(kon), str(kon))
        self.assertEqual(len(kon2), 5)
        
if __name__ == '__main__': 
    unittest.main() 