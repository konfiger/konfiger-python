
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
        self.enable_cache_ = True
        self.prev_cache_object = { "ckey": "", "cvalue": None }
        self.current_cache_object = { "ckey": "", "cvalue": None }
        
        if not self.lazy_load:
            self.lazy_loader()
         
        if not is_bool(lazy_load):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument expecting boolean found " + str(type(lazy_load)))            
        
    def put(self, key, value):
        if is_string(key):
            if self.attached_resolve_obj is not None:
                pass
            
            if is_string(value):
                self.put_string(key, value)
            elif is_bool(value):
                self.put_boolean(key, value)
            else:
                self.put_string(key, str(value))
        else:
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be string found " + str(type(key)))
        
    def put_string(self, key, value):
        global MAX_CAPACITY
        if not is_string(key):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be string found " + str(type(key)))
        if not is_string(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be string found " + str(type(value)))
            
        if key not in self.konfiger_objects:
            if len(self.konfiger_objects) >= MAX_CAPACITY:
                raise TypeError("io.github.thecarisma.konfiger: konfiger has reached it maximum capacity of " + MAX_CAPACITY)
        
        self.konfiger_objects[key] = value
        self.changes_occur = True
        if self.enable_cache_:
            self.shift_cache(key, value)
        
    def put_boolean(self, key, value):
        if not is_bool(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be bool found " + str(type(value)))
        self.put_string(key, str(value))
        
    def put_long(self, key, value):
        if not is_number(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be a number found " + str(type(value)))
        self.put_string(key, str(value))
        
    def put_int(self, key, value):
        self.put_long(key, value)
        
    def put_float(self, key, value):
        if not is_float(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be a floating type found " + str(type(value)))
        self.put_string(key, str(value))
        
    def put_double(self, key, value):
        self.put_float(key, value)
        
    def put_comment(self, the_comment):
        self.put_string(self.stream.get_comment_prefix(), the_comment)
        
    def get(self, key, default_value=None):
        if not is_string(key):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be a string found " + str(type(key)))
            
        if self.enable_cache_:
            if self.current_cache_object["ckey"] == key:
                return self.current_cache_object["cvalue"]
            if self.prev_cache_object["ckey"] == key:
                return self.prev_cache_object["cvalue"]
                
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
        if default_value is not None and key not in self.konfiger_objects:
            value = str(default_value)
        elif key in self.konfiger_objects:
            value = self.konfiger_objects[key]
            if self.enable_cache_:
                self.shift_cache(key, value)
        
        return value
        
    def get_string(self, key, default_value=None):
        value = self.get(key, default_value)
        return value if value is not None else default_value
        
    def get_boolean(self, key, default_value=None):
        value = self.get(key, default_value)
        return value.lower() == "true" if value is not None else False
        
    def get_long(self, key, default_value=None):
        value = self.get(key, default_value)
        return int(value) if value is not None else default_value
        
    def get_int(self, key, default_value=None):
        return self.get_long(key, default_value)
        
    def get_float(self, key, default_value=None):
        value = self.get(key, default_value)
        return float(value) if value is not None else default_value
        
    def get_double(self, key, default_value=None):
        return self.get_float(key, default_value)
        
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
        if not is_string(key):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be a string found " + str(type(key)))
            
        if key in self.konfiger_objects:
            return True
        if not self.loading_ends and self.lazy_load:
            self.changes_occur = True
            while self.stream.has_next():
                obj = self.stream.next()
                self.konfiger_objects[obj[0]] = obj[1]
                if obj[0] == key:
                    return True
            self.loading_ends = True
        
        return False
        
    def keys(self):
        if not self.loading_ends and self.lazy_load:
            self.lazy_loader()
        
        return self.konfiger_objects.keys()
        
    def values(self):
        if not self.loading_ends and self.lazy_load:
            self.lazy_loader()
        
        return self.konfiger_objects.values()
        
    def entries(self):
        if not self.loading_ends and self.lazy_load:
            self.lazy_loader()
        
        return self.konfiger_objects.items()
        
    def clear(self):
        self.changes_occur = True
        self.enable_cache(self.enable_cache_)
        self.konfiger_objects.clear()
        
    def remove(self, key_index):
        pass
        
    def update_at(self, index, value):
        pass
        
    def size(self):
        if not self.loading_ends and self.lazy_load:
            self.lazy_loader()
        
        return len(self.konfiger_objects)
        
    def is_empty(self):
        return self.size() == 0
        
    def get_seperator(self):
        return self.seperator
        
    def set_seperator(self, seperator):
        if not is_char(seperator):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, seperator must be a char found " + str(type(seperator)))
            
        if self.seperator != seperator:
            self.changes_occur = True
            old_seperator = self.seperator
            self.seperator = seperator
            for key, value in self.konfiger_objects.items():
                self.konfiger_objects[key] = un_escape_string(value, seperator)
        
    def get_delimeter(self):
        return self.delimeter
        
    def set_delimeter(self, delimeter):
        if not is_char(delimeter):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, delimeter must be a char found " + str(type(delimeter)))
            
        self.changes_occur = True
        self.delimeter = delimeter
        
    def is_case_sensitive(self):
        return self.case_sensitive
        
    def set_case_sensitivity(self, case_sensitive):
        if not is_bool(case_sensitive):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, case_sensitive must be a bool found " + str(type(case_sensitive)))
            
        self.case_sensitive = case_sensitive
        
    def hash_code(self):
        if self.hashcode != 0:
            return self.hashcode
            
        c = '\0'
        if len(self.string_value) == 0:
            self.string_value = self.__str__()
        for i in range(len(self.string_value)):
            c = ord(self.string_value[i])
            self.hashcode = ((self.hashcode << 5) - self.hashcode) + c
            self.hashcode = self.hashcode | 0
        
        return self.hashcode
        
    def __str__(self):
        if self.changes_occur:
            if not self.loading_ends and self.lazy_load:
                self.lazy_loader()
            
            self.string_value = ""
            index = 0
            for key, value in self.konfiger_objects.items():
                if key is None:
                    continue
                self.string_value = self.string_value + key + self.delimeter + escape_string(value, self.seperator)
                index = index + 1
                if index < len(self.konfiger_objects):
                    self.string_value = self.string_value + self.seperator
            self.changes_occur = False
            
        return self.string_value
        
    def lazy_loader(self):
        if self.loading_ends:
            return
        
        while self.stream.has_next():
            obj = self.stream.next()
            self.put_string(obj[0], obj[1])
        self.loading_ends = True
        
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