#!python {0}

import unittest 
import os
import sys
sys.path.insert(0, os.getcwd())
from src import from_file, from_string, from_stream, file_stream, string_stream

class TextsFlat:
    project = None
    Platform = None
    File = None
    author = None

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
        texts_flat = TextsFlat
        kon.resolve(texts_flat)
        
        self.assertEqual(texts_flat.project, None)
        self.assertEqual(texts_flat.Platform, "Cross Platform")
        self.assertEqual(texts_flat.File, "test.comment.inf")
        self.assertEqual(texts_flat.author, None)

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass

    def test_(self):
        pass
        
if __name__ == '__main__': 
    unittest.main() 