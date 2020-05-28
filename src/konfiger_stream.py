
"""
    The MIT License
    Copyright 2020 Adewale Azeez <azeezadewale98@gmail.com>.
"""

import os.path
from .konfiger_util import type_of, is_string, is_char, is_boolean

def file_stream(file_path, delimeter = '=', seperator = '\n', err_tolerance = False):
    return KonfigerStream(file_path, delimeter, seperator, err_tolerance, True)

def string_stream(raw_string, delimeter = '=', seperator = '\n', err_tolerance = False):
    return KonfigerStream(raw_string, delimeter, seperator, err_tolerance, False)
    
def validate_file_existence(file_path):
    if not file_path:
        raise TypeError("The file path cannot be null")
    if not is_string(file_path):
        raise TypeError("Invalid argument expecting str found " + str(type(file_path)))
    if not os.path.isfile(file_path):
        raise FileNotFoundError("The file does not exists: " + file_path)

class KonfigerStream:

    def __init__(self, stream_obj, delimeter, seperator, err_tolerance, is_file):
        self.stream_obj = stream_obj
        self.delimeter = delimeter
        self.seperator = seperator
        self.err_tolerance = err_tolerance
        self.is_file = is_file
        
        if is_file:
            validate_file_existence(stream_obj)
        else:
            if not is_string(stream_obj):
                raise TypeError("Invalid argument expecting str found " + str(type(stream_obj)))
        if not is_boolean(err_tolerance):
            raise TypeError("Invalid argument for errTolerance expecting boolean found " + str(type(stream_obj)))
        if delimeter and not seperator:
            raise TypeError("Invalid length of argument, seperator or delimeter parameter is missing")
        if not is_char(self.delimeter):
            raise TypeError("Invalid argument for delimeter expecting char found " + str(type(stream_obj)))
        if not is_char(self.seperator):
            raise TypeError("Invalid argument for seperator expecting char found " + str(type(stream_obj)))
        
        self.read_position = 0
        self.has_next_ = False
        self.done_reading_ = False



