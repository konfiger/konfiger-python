
"""
    The MIT License
    Copyright 2020 Adewale Azeez <azeezadewale98@gmail.com>.
"""

from .konfiger_stream import file_stream, string_stream
from .konfiger_util import type_of, is_string, is_char, is_bool, escape_string, un_escape_string

max_capacity = 10000000

def from_file(file_path, lazy_load=True, delimeter='=', seperator='\n'):
    kon = from_stream(file_stream(file_path, delimeter, seperator), lazy_load)
    kon.filePath = kon.stream.stream_obj
    return kon

def from_string(raw_string, lazy_load=True, delimeter='=', seperator='\n'):
    return from_stream(string_stream(raw_string, delimeter, seperator), lazy_load)

def from_stream(konfiger_stream, lazy_load=True):
    if not is_bool(lazy_load):
        lazy_load = True
    return Konfiger(konfiger_stream, lazy_load)

class Konfiger:

    def __init__(self, stream, lazy_load):
        self.hashcode = 0
        self.stream = stream
        self.loading_ends = False
        self.lazy_load = lazy_load
        self.konfiger_objects = {}
        self.delimeter = stream.delimeter
        self.seperator = stream.seperator
        self.case_sensitive = True
        self.changes_occur = True
        self.string_value = ""
        self.read_index = 0
        self.file_path = None
        self.attached_resolve_obj = None
        
        if not self.lazy_load:
            self.lazy_loader()
         
        if not is_bool(lazy_load):
            raise TypeError("Invalid argument expecting boolean found " + str(type(lazy_load)))
        
    def put(self, key, value):
        pass
        
    def put_string(self, key, value):
        pass
        
    def put_boolean(self, key, value):
        pass
        
    def put_long(self, key, value):
        pass
        
    def put_int(self, key, value):
        pass
        
    def put_float(self, key, value):
        pass
        
    def put_double(self, key, value):
        pass
        
    def put_comment(self, the_comment):
        pass
        
    def get(self, key, default_value):
        pass
        
    def get_string(self, key, default_value):
        pass
        
    def get_boolean(self, key, default_value):
        pass
        
    def get_long(key, default_value):
        pass
        
    def get_int(key, default_value):
        pass
        
    def get_float(key, default_value):
        pass
        
    def get_double(key, default_value):
        pass
        
    def shift_cache(key, value):
        pass
        
    def enable_cache(enable_cache_):
        pass
        
    def contains(self, key):
        pass
        
    def keys(self):
        pass
        
    def values(self):
        pass
        
    def entries(self):
        pass
        
    def clear(self):
        pass
        
    def remove(self, key_index):
        pass
        
    def update_at(self, index, value):
        pass
        
    def size(self):
        pass
        
    def is_empty(self):
        pass
        
    def get_seperator(self):
        pass
        
    def set_seperator(self, seperator):
        pass
        
    def get_delimeter(self, delimeter):
        pass
        
    def set_delimeter(self):
        pass
        
    def error_tolerance(self, err_tolerance):
        pass
        
    def is_error_tolerant(self):
        pass
        
    def hash_code(self):
        pass
        
    def to_string(self):
        pass
        
    def lazy_loader(self):
        pass
        
    def save(file_path=None):
        pass
        
    def append_string(self, raw_string, delimeter, seperator):
        pass
        
    def append_file(self, file_path, delimeter, seperator):
        pass
        
    def resolve(self, obj):
        pass
        
    def dissolve(self, obj):
        pass
        
    def detach(self):
        pass