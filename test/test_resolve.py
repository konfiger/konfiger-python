#!python {0}

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import from_file, from_string, from_stream, file_stream, string_stream, konfiger_values

class TextsFlat:
    project = ""
    Platform = ""
    File = ""
    author = ""

class Texts:
    project = ""
    Platform = ""
    file = ""
    author = ""
    
    def match_get_key(self, key):
        if key == "project":
            return "Project"
        elif key == "author":
            return "Author"
        elif key == "file":
            return "File"
    
    def match_put_key(self, key):
        if key == "Project":
            return "project"
        elif key == "Author":
            return "author"
        elif key == "File":
            return "file"

@konfiger_values({
    "Project": "project",
    "Author": "author",
    "File": "file"
})
class DecoratedTexts:
    project = ""
    Platform = ""
    file = ""
    author = ""
            
class Entries:
    project = "konfiger"
    author = "Adewale Azeez"
    platform = "Cross Platform"
    file = "test.comment.inf"
      
@konfiger_values({
    "Project": "project",
    "Author": "author",
    "Platform": "platform",
    "File": "file"
})      
class DecoratedEntries:
    project = "konfiger"
    author = "Adewale Azeez"
    platform = "Cross Platform"
    file = "test.comment.inf"
    
class MixedTypes:
    project = ""
    weAllCake = False
    annotatedEntry = False
    ageOfEarth = 0
    lengthOfRiverNile = 0
    pi = 0.0
    pie = 0.0
    
    def match_get_key(self, key):
        if key == "annotatedEntry":
            return "AnnotatedEntry"

    def match_put_key(self, key):
        if key == "AnnotatedEntry":
            return "annotatedEntry"
            
class MixedTypesEntries:
    project = "konfiger"
    weAllCake = True
    ageOfEarth = 121526156252322
    lengthOfRiverNile = 45454545
    pi = 3.14
    pie = 1.1121

class TestKonfigerResolve(unittest.TestCase): 

    def test_invalid_argument_type_to_Konfiger_resolve(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        
        with self.assertRaises(TypeError) as context:
            kon.resolve(123)
        self.assertTrue('io.github.thecarisma.konfiger: Invalid argument, the parameter must be a class object found ' in str(context.exception))

    def test_resolve_without_match_get_key_function(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        texts_flat = TextsFlat()
        kon.resolve(texts_flat)
        
        self.assertEqual(texts_flat.project, "")
        self.assertEqual(texts_flat.Platform, "Cross Platform")
        self.assertEqual(texts_flat.File, "test.comment.inf")
        self.assertEqual(texts_flat.author, "")

    def test_resolve_with_match_get_key_function(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        texts = Texts()
        kon.resolve(texts)
        
        self.assertEqual(texts.project, "konfiger")
        self.assertEqual(texts.Platform, "Cross Platform")
        self.assertEqual(texts.file, "test.comment.inf")
        self.assertEqual(texts.author, "Adewale Azeez")

    def test_resolve_with_changing_values_and_map_key_with_match_put_key(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        texts = Texts()
        kon.resolve(texts)
        
        self.assertEqual(texts.project, "konfiger")
        self.assertEqual(texts.Platform, "Cross Platform")
        self.assertEqual(texts.file, "test.comment.inf")
        self.assertEqual(texts.author, "Adewale Azeez")
        
        kon.put("Project", "konfiger-nodejs")
        kon.put("Platform", "Windows, Linux, Mac, Raspberry")
        kon.put("author", "Thecarisma")
        
        self.assertEqual(texts.project, "konfiger-nodejs")
        self.assertEqual("Windows" in texts.Platform, True)
        self.assertEqual("Linux" in texts.Platform, True)
        self.assertEqual("Mac" in texts.Platform, True)
        self.assertEqual("Raspberry" in texts.Platform, True)
        self.assertEqual(texts.author, "Thecarisma")

    def test_resolve_with_changing_values_and_map_key_with_match_put_key_using_decorator(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        texts = DecoratedTexts()
        kon.resolve(texts)
        
        self.assertEqual(texts.project, "konfiger")
        self.assertEqual(texts.Platform, "Cross Platform")
        self.assertEqual(texts.file, "test.comment.inf")
        self.assertEqual(texts.author, "Adewale Azeez")
        
        kon.put("Project", "konfiger-nodejs")
        kon.put("Platform", "Windows, Linux, Mac, Raspberry")
        kon.put("author", "Thecarisma")
        
        self.assertEqual(texts.project, "konfiger-nodejs")
        self.assertEqual("Windows" in texts.Platform, True)
        self.assertEqual("Linux" in texts.Platform, True)
        self.assertEqual("Mac" in texts.Platform, True)
        self.assertEqual("Raspberry" in texts.Platform, True)
        self.assertEqual(texts.author, "Thecarisma")

    def test_dissolve_an_object_into_konfiger(self):
        kon = from_string("")
        kon.dissolve(Entries())
        
        self.assertEqual(kon.get("project"), "konfiger")
        self.assertEqual(kon.get("platform"), "Cross Platform")
        self.assertEqual(kon.get("file"), "test.comment.inf")
        self.assertEqual(kon.get("author"), "Adewale Azeez")

    def test_dissolve_an_object_into_konfiger_using_decorator(self):
        kon = from_string("")
        kon.dissolve(DecoratedEntries())
        
        self.assertEqual(kon.get("Project"), "konfiger")
        self.assertEqual(kon.get("Platform"), "Cross Platform")
        self.assertEqual(kon.get("File"), "test.comment.inf")
        self.assertEqual(kon.get("Author"), "Adewale Azeez")

    def test_detach_an_object_from_konfiger(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        texts = Texts()
        kon.resolve(texts)
        
        self.assertEqual(texts.project, "konfiger")
        self.assertEqual(texts.Platform, "Cross Platform")
        self.assertEqual(texts.file, "test.comment.inf")
        self.assertEqual(texts.author, "Adewale Azeez")
        self.assertEqual(texts, kon.detach())
        
        kon.put("Project", "konfiger-nodejs")
        kon.put("Platform", "Windows, Linux, Mac, Raspberry")
        kon.put("author", "Thecarisma")
        
        self.assertNotEqual(texts.project, "konfiger-nodejs")
        self.assertNotEqual("Windows" in texts.Platform, True)
        self.assertNotEqual("Linux" in texts.Platform, True)
        self.assertNotEqual("Mac" in texts.Platform, True)
        self.assertNotEqual("Raspberry" in texts.Platform, True)
        self.assertNotEqual(texts.author, "Thecarisma")

    def test_resolve_with_matchGetKey_function_mixed_types(self):
        kon = from_file('test/mixed.types')
        mixedTypes = MixedTypes()
        kon.resolve(mixedTypes)
        
        self.assertEqual(mixedTypes.project, "konfiger")
        self.assertNotEqual(mixedTypes.weAllCake, "true")
        self.assertEqual(mixedTypes.weAllCake, True)
        self.assertEqual(mixedTypes.annotatedEntry, True)
        self.assertNotEqual(mixedTypes.ageOfEarth, "121526156252322")
        self.assertEqual(mixedTypes.ageOfEarth, 121526156252322)
        self.assertNotEqual(mixedTypes.lengthOfRiverNile, "45454545")
        self.assertEqual(mixedTypes.lengthOfRiverNile, 45454545)
        self.assertNotEqual(mixedTypes.pi, "3.14")
        self.assertEqual(mixedTypes.pi, 3.14)
        self.assertNotEqual(mixedTypes.pie, "1.1121")
        self.assertEqual(mixedTypes.pie, 1.1121)

    def test_dissolve_an_mixed_types_object_into_konfiger(self):
        kon = from_file('test/mixed.types')
        kon.dissolve(MixedTypesEntries)
        
        self.assertEqual(kon.get("project"), "konfiger")
        self.assertEqual(kon.get_string("weAllCake"), "True")
        self.assertEqual(kon.get_boolean("weAllCake"), True)
        self.assertEqual(kon.get("ageOfEarth"), "121526156252322")
        self.assertEqual(kon.get_long("ageOfEarth"), 121526156252322)
        self.assertEqual(kon.get("lengthOfRiverNile"), "45454545")
        self.assertEqual(kon.get_int("lengthOfRiverNile"), 45454545)
        self.assertEqual(kon.get("pi"), "3.14")
        self.assertEqual(kon.get_float("pi"), 3.14, 1)
        self.assertEqual(kon.get("pie"), "1.1121")
        self.assertEqual(kon.get_double("pie"), 1.1121, 1)

    def test_resolve_with_changing_values_for_mixed_types(self):
        kon = from_file('test/mixed.types')
        mixedTypes = MixedTypes()
        kon.resolve(mixedTypes)
        
        self.assertEqual(mixedTypes.project, "konfiger")
        self.assertEqual(mixedTypes.weAllCake, True)
        self.assertEqual(mixedTypes.ageOfEarth, 121526156252322)
        self.assertEqual(mixedTypes.lengthOfRiverNile, 45454545)
        self.assertEqual(mixedTypes.pi, 3.14, 1)
        self.assertEqual(mixedTypes.pie, 1.1121, 1)
        self.assertEqual(mixedTypes.annotatedEntry, True)

        kon.put("project", "konfiger-nodejs")
        kon.put("AnnotatedEntry", False)
        kon.put("ageOfEarth", 121323)
        kon.put("pie", 2.1212)

        self.assertEqual(mixedTypes.project, "konfiger-nodejs")
        self.assertEqual(mixedTypes.annotatedEntry, False)
        self.assertEqual(mixedTypes.ageOfEarth, 121323)
        self.assertEqual(mixedTypes.pie, 2.1212, 1)

        kon.put("AnnotatedEntry", True)
        self.assertEqual(mixedTypes.annotatedEntry, True)

    def test_resolve_with_changing_values_and_map_key_with_attach(self):
        kstream = file_stream('test/test.comment.inf')
        kstream.set_comment_prefix("[")
        kon = from_stream(kstream)
        texts = Texts()
        kon.attach(texts)
        
        self.assertNotEqual(texts.project, "konfiger")
        self.assertNotEqual(texts.Platform, "Cross Platform")
        self.assertNotEqual(texts.file, "test.comment.inf")
        self.assertNotEqual(texts.author, "Adewale Azeez")
        
        kon.put("Project", "konfiger-nodejs")
        kon.put("Platform", "Windows, Linux, Mac, Raspberry")
        kon.put("author", "Thecarisma")
        
        self.assertEqual(texts.project, "konfiger-nodejs")
        self.assertEqual("Windows" in texts.Platform, True)
        self.assertEqual("Linux" in texts.Platform, True)
        self.assertEqual("Mac" in texts.Platform, True)
        self.assertEqual("Raspberry" in texts.Platform, True)
        self.assertEqual(texts.author, "Thecarisma")
        
if __name__ == '__main__': 
    unittest.main() 