
"""
    The MIT License
    Copyright 2020 Adewale Azeez <azeezadewale98@gmail.com>.
"""

from .konfiger_stream import file_stream, string_stream
from .konfiger_util import type_of, is_string, is_char, is_bool, is_number, is_float, is_object, escape_string, un_escape_string

MAX_CAPACITY = 10000000

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
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument expecting boolean found " + str(type(lazy_load)))
            
        self.enable_cache_ = True
        self.prev_cache_object = { "ckey": "", "cvalue": None }
        self.current_cache_object = { "ckey": "", "cvalue": None }
        
    def put(self, key, value):
        if is_string(key):
            if self.attached_resolve_obj is not None:
                pass
            
            if is_string(value):
                put_string(key, value)
            elif is_bool(value):
                put_boolean(key, value)
            else:
                put_string(key, str(value))
        else:
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be string found " + str(type(key)))
        
    def put_string(self, key, value):
        global MAX_CAPACITY
        if not is_string(key):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be string found " + str(type(key)))
        if not is_string(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be string found " + str(type(value)))
        if key not in konfiger_objects:
            if len(konfiger_objects) >= MAX_CAPACITY:
                raise TypeError("io.github.thecarisma.konfiger: konfiger has reached it maximum capacity of " + MAX_CAPACITY)
        
    def put_boolean(self, key, value):
        if not is_bool(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be bool found " + str(type(value)))
        put_string(key, str(value))
        
    def put_long(self, key, value):
        if not is_number(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be a number found " + str(type(value)))
        put_string(key, str(value))
        
    def put_int(self, key, value):
        put_long(key, value)
        
    def put_float(self, key, value):
        if not is_float(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be a floating type found " + str(type(value)))
        put_string(key, str(value))
        
    def put_double(self, key, value):
        put_float(key, value)
        
    def put_comment(self, the_comment):
        put_string(self.stream.get_comment_prefix(), the_comment)
        
    def get(self, key, default_value=None):
        if not is_string(key):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be a string found " + str(type(key)))
            
        if self.enable_cache_:
            if self.current_cache_object["ckey"] == key:
                return self.current_cache_object["value"]
            if self.prev_cache_object["ckey"] == key:
                return self.prev_cache_object["value"]
                
        if key not in self.konfiger_objects and self.lazy_load:
            if not self.loading_ends:
                self.changes_occur = True
                while self.stream.has_next():
                    obj = self.stream.next()
                    self.konfiger_objects[obj[0]] = obj[1]
                    if obj[0] == key:
                        if self.enable_cache_:
                            self.shift_cache(key, obj[1])
                        return obj[1]
                self.loading_ends = True
                
        if not self.case_sensitive:
            for entry_key, entry_value in self.konfiger_objects.items():
                if entry_key.lower() == key.lower():
                    key = entry_key
                    if self.enable_cache_:
                        self.shift_cache(key, value)
                    return entry_value
        
        value = None   
        if default_value is not None and key in self.konfiger_objects:
            value = str(default_value)
        elif key in self.konfiger_objects:
            value = self.konfiger_objects[key]
            if self.enable_cache_:
                self.shift_cache(key, value)
        return value
        
    def get_string(self, key, default_value=None):
        value = get(key, default_value)
        return value if value is not None else default_value
        
    def get_boolean(self, key, default_value=None):
        value = get(key, default_value)
        return value.lower() == "true" if value is not None else False
        
    def get_long(self, key, default_value=None):
        value = get(key, default_value)
        return int(value) if value is not None else default_value
        
    def get_int(self, key, default_value=None):
        return get_long(key, default_value)
        
    def get_float(self, key, default_value=None):
        value = get(key, default_value)
        return float(value) if value is not None else default_value
        
    def get_double(self, key, default_value=None):
        return get_float(key, default_value)
        
    def shift_cache(self, key, value):
        self.prev_cache_object = self.current_cache_object
        self.current_cache_object = { "ckey": key, "cvalue": value }
        
    def enable_cache(self, enable_cache_):
        if not is_bool(enable_cache_):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, argument must be a bool found " + str(type(enable_cache_)))
        
        self.prev_cache_object = { "ckey": "", "cvalue": None }
        self.current_cache_object = { "ckey": "", "cvalue": None }
        self.enable_cache_ = enable_cache_
        
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