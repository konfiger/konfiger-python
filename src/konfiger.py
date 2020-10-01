
"""
    The MIT License
    Copyright 2020 Adewale Azeez <azeezadewale98@gmail.com>.
"""

from .konfiger_stream import file_stream, string_stream
from .konfiger_util import type_of, is_string, is_char, is_bool, is_number, is_float, escape_string, un_escape_string

GLOBAL_MAX_CAPACITY = 10000000

def konfiger_values(argument):
    def match_get_key(self, key):
        for inkey, value in argument.items():
            if value == key:
                return inkey
    def match_put_key(self, key):
        if key in argument.keys():
            return argument[key]
    def mutated_class(klazz):
        setattr(klazz, "match_get_key", match_get_key)
        setattr(klazz, "match_put_key", match_put_key)
        return klazz
    return mutated_class

def from_file(file_path, lazy_load=True, delimeter='=', seperator='\n'):
    kon = from_stream(file_stream(file_path, delimeter, seperator), lazy_load)
    kon.file_path = kon.stream.stream_obj
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
            if is_string(value):
                self.put_string(key, value)
            elif is_bool(value):
                self.put_boolean(key, value)
            else:
                self.put_string(key, str(value))
        else:
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be string found " + str(type(key)))
        
    def put_string(self, key, value):
        global GLOBAL_MAX_CAPACITY
        if not is_string(key):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key must be string found " + str(type(key)))
        if not is_string(value):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, value must be string found " + str(type(value)))
            
        if key not in self.konfiger_objects:
            if len(self.konfiger_objects) >= GLOBAL_MAX_CAPACITY:
                raise TypeError("io.github.thecarisma.konfiger: konfiger has reached it maximum capacity of " + GLOBAL_MAX_CAPACITY)
        
        self.konfiger_objects[key] = value
        if self.attached_resolve_obj is not None:
            find_key = None
            match_put_key = getattr(self.attached_resolve_obj, "match_put_key", None)
            if callable(match_put_key):
                find_key = match_put_key(key)
            if find_key is None:
                if hasattr(self.attached_resolve_obj, key):
                    find_key = key
            if find_key is not None:
                field = getattr(self.attached_resolve_obj, find_key, None)
                if not callable(field):
                    if is_string(field):
                        setattr(self.attached_resolve_obj, find_key, value)
                    elif is_bool(field):
                        setattr(self.attached_resolve_obj, find_key, value.lower() == "true")
                    elif is_float(field):
                        setattr(self.attached_resolve_obj, find_key, float(value))
                    elif is_number(field):
                        setattr(self.attached_resolve_obj, find_key, int(value))
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
                        self.shift_cache(key, entry_value)
                    return entry_value
        
        value = None   
        if default_value is not None and key not in self.konfiger_objects:
            value = str(default_value)
        elif key in self.konfiger_objects:
            value = self.konfiger_objects[key]
            if self.enable_cache_:
                self.shift_cache(key, value)
        
        return value
        
    def get_string(self, key, default_value=""):
        value = self.get(key, default_value)
        return value if value is not None else default_value
        
    def get_boolean(self, key, default_value=False):
        value = self.get(key, default_value)
        return value.lower() == "true" if value is not None else False
        
    def get_long(self, key, default_value=0):
        value = self.get(key, default_value)
        return int(value) if value is not None else default_value
        
    def get_int(self, key, default_value=0):
        return self.get_long(key, default_value)
        
    def get_float(self, key, default_value=0.0):
        value = self.get(key, default_value)
        return float(value) if value is not None else default_value
        
    def get_double(self, key, default_value=0.0):
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
        if is_string(key_index):
            self.changes_occur = True
            if key_index in self.konfiger_objects.keys():
                enable_cache_ = self.enable_cache_
                self.enable_cache(False)
                ret = self.get(key_index)
                self.enable_cache(enable_cache_)
                del self.konfiger_objects[key_index]
                if key_index not in self.konfiger_objects.keys():
                    return ret
                return None
                
        elif is_number(key_index):
            if key_index < len(self.konfiger_objects):
                index = -1
                for key in self.konfiger_objects.keys():
                    index = index + 1
                    if index == key_index:
                        return self.remove(key)
                return None
            
        else:
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, key_index must be a string or number found " + str(type(key_index)))
        
    def update_at(self, index, value):
        if is_number(index) and is_string(value):
            if index < len(self.konfiger_objects):
                i = -1
                for key in self.konfiger_objects.keys():
                    i = i + 1
                    if i == index:
                        self.changes_occur = True
                        self.enable_cache(self.enable_cache_)
                        self.konfiger_objects[key] = value
                        break
        else:
            raise TypeError("io.github.thecarisma.Konfiger: Invalid argument, expecting the entry (<class 'int'>, <class 'str'>) found (" + str(type(index)) + ", " + str(type(value)) + ")")
        
    def __len__(self):
        if not self.loading_ends and self.lazy_load:
            self.lazy_loader()
        
        return len(self.konfiger_objects)
        
    def is_empty(self):
        return self.__len__() == 0
        
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
        
    def save(self, file_path=None):
        if self.file_path is None and file_path is None:
            raise TypeError("io.github.thecarisma.Konfiger: The entries cannot be saved you need to specify the file_path as parameter or load Konfiger from a file")
            
        if file_path is None:
            file_path = self.file_path
        with open(file_path, 'w') as file:
            file.write(self.__str__())
        
    def append_string(self, raw_string, delimeter=None, seperator=None):
        if delimeter is None:
            delimeter = self.delimeter
        if seperator is None:
            seperator = self.seperator
        
        stream_ = string_stream(raw_string, delimeter, seperator)
        while stream_.has_next():
            obj = stream_.next()
            self.put_string(obj[0], obj[1])
        self.changes_occur = True
        
    def append_file(self, file_path, delimeter=None, seperator=None):
        if delimeter is None:
            delimeter = self.delimeter
        if seperator is None:
            seperator = self.seperator
        
        stream_ = file_stream(file_path, delimeter, seperator)
        while stream_.has_next():
            obj = stream_.next()
            self.put_string(obj[0], obj[1])
        self.changes_occur = True
        
    def resolve(self, obj):
        if is_string(obj) or is_number(obj) or is_bool(obj) or is_char(obj):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, the parameter must be a class object found " + str(type(obj)))
            
        self.attached_resolve_obj = obj
        fields = dir(obj)
        for key in fields:
            value = getattr(obj, key)
            if not callable(value) and not key.startswith("__"):
                find_key = key
                match_get_key = getattr(obj, "match_get_key", None)
                if callable(match_get_key):
                    find_key = match_get_key(key)
                    if find_key is None:
                        find_key = key
                if self.contains(find_key):
                    if is_string(value):
                        setattr(obj, key, self.get(find_key))
                    elif is_bool(value):
                        setattr(obj, key, self.get_boolean(find_key))
                    elif is_float(value):
                        setattr(obj, key, self.get_float(find_key))
                    elif is_number(value):
                        setattr(obj, key, self.get_long(find_key))
        
    def dissolve(self, obj):
        if is_string(obj) or is_number(obj) or is_bool(obj) or is_char(obj):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, the parameter must be a class object found " + str(type(obj)))
            
        fields = dir(obj)
        for key in fields:
            value = getattr(obj, key)
            if not callable(value) and not key.startswith("__"):
                find_key = key
                match_get_key = getattr(obj, "match_get_key", None)
                if callable(match_get_key):
                    find_key = match_get_key(key)
                    if find_key is None:
                        find_key = key
                if find_key is not None:
                    self.put_string(find_key, str(value))
        
    def attach(self, obj):
        if is_string(obj) or is_number(obj) or is_bool(obj) or is_char(obj):
            raise TypeError("io.github.thecarisma.konfiger: Invalid argument, the parameter must be a class object found " + str(type(obj)))
        self.attached_resolve_obj = obj
        
    def detach(self):
        tmp_obj = self.attached_resolve_obj
        self.attached_resolve_obj = None
        return tmp_obj



