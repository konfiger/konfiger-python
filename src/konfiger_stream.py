
"""
    The MIT License
    Copyright 2020 Adewale Azeez <azeezadewale98@gmail.com>.
"""

import os.path
from .konfiger_util import type_of, is_string, is_char, is_bool, escape_string, un_escape_string

def file_stream(file_path, delimeter = '=', seperator = '\n', err_tolerance = False):
    return KonfigerStream(file_path, delimeter, seperator, err_tolerance, True)

def string_stream(raw_string, delimeter = '=', seperator = '\n', err_tolerance = False):
    return KonfigerStream(raw_string, delimeter, seperator, err_tolerance, False)
    
def validate_file_existence(file_path):
    if not file_path:
        raise TypeError("The file path cannot be None")
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
        self.triming_key = True
        self.comment_prefix = "//"
        self.is_first = 0
        
        if is_file:
            validate_file_existence(stream_obj)
        else:
            if not is_string(stream_obj):
                raise TypeError("Invalid argument expecting str found " + str(type(stream_obj)))
        if not is_bool(err_tolerance):
            raise TypeError("Invalid argument for err_tolerance expecting bool found " + str(type(stream_obj)))
        if delimeter and not seperator:
            raise TypeError("Invalid length of argument, seperator or delimeter parameter is missing")
        if not is_char(self.delimeter):
            raise TypeError("Invalid argument for delimeter expecting char found " + str(type(stream_obj)))
        if not is_char(self.seperator):
            raise TypeError("Invalid argument for seperator expecting char found " + str(type(stream_obj)))
        
        self.read_position = 0
        self.has_next_ = False
        self.done_reading_ = False

    def is_trimming_key(self):
        return self.triming_key
        
    def set_triming_key(self, triming_key):
        if not is_bool(triming_key):
            raise TypeError("Invalid argument for delimeter expecting bool found " + str(type(stream_obj)))
        self.triming_key = triming_key
        
    def get_comment_prefix(self):
        return self.comment_prefix
        
    def set_comment_prefix(self, comment_prefix):
        if not is_string(comment_prefix):
            raise TypeError("Invalid argument for delimeter expecting str found " + str(type(stream_obj)))
        self.comment_prefix = comment_prefix
        
    def has_next(self):
        if not self.done_reading_:
            comment_size = len(self.comment_prefix)
            sub_count = 0
            if self.is_file:
                with open(self.stream_obj, "r") as f:
                    byte = f.read(1)
                    f.seek(self.read_position)
                    if not byte:
                        self.done_reading()
                        return self.has_next_ 
                    while byte:
                        byte = f.read(1)
                        while sub_count < comment_size and byte == self.comment_prefix[sub_count]:
                            sub_count += 1
                            f.seek(self.read_position+sub_count)
                            byte = f.read(1)
                        self.is_first |= 1
                        if sub_count == comment_size:
                            self.read_position += 1
                            while byte and byte != self.seperator:
                                self.read_position += 1
                                f.seek(self.read_position)
                                byte = f.read(1)
                            return self.has_next()
                        if byte.strip() == '':
                            self.read_position += 1
                            f.seek(self.read_position)
                            continue
                        self.hasNext_ = True
                        return self.hasNext_
                self.has_next_ = False 
                return self.has_next_ 
            else:
                while self.read_position < len(self.stream_obj):
                    while (self.stream_obj[sub_count+self.read_position] == self.comment_prefix[sub_count]):
                        sub_count += 1
                    if sub_count == comment_size:
                        self.read_position += 1
                        while self.read_position < len(self.stream_obj) and self.stream_obj[self.read_position] != self.seperator:
                            self.read_position += 1
                        self.read_position += 1
                        return self.has_next()
                    if self.stream_obj[self.read_position].strip() == "":
                        self.read_position += 1
                        continue         
                self.has_next_ = False 
                return self.has_next_ 
                    
        return self.has_next_
    
    def next(self):
        if self.done_reading_:
            raise BufferError("You cannot read beyound the stream length, always use hasNext() to verify the Stream still has an entry")
        key = ""
        value = ""
        parse_key = True
        prev_char = None
        line = 1
        column = 0
        
        if self.is_file:
            with open(self.stream_obj, "r") as f:
                while True:
                    byte = f.read(1)
                    f.seek(self.read_position)
                    if not byte:
                        if key != "":
                            if parse_key == True and self.err_tolerance == False:
                                raise LookupError("Invalid entry detected near Line " + str(line) + ":"  + str(column))
                        self.done_reading()
                        break
                    self.read_position += 1
                    char_ = f.read(1)
                    column += 1
                    if char_ == '\n':
                        line += 1
                        column = 0 
                    if char_ == self.seperator and prev_char != '\\' and not parse_key:
                        if value == "":
                            continue
                        if parse_key == True and self.err_tolerance == False:
                            raise LookupError("Invalid entry detected near Line " + str(line) + ":"  + str(column))
                        break
                    if char_ == self.delimeter and parse_key:
                        if value != "" and self.err_tolerance != False:
                            raise LookupError("The input is imporperly sepreated near Line " + str(line) + ":"  + str(column)+". Check the separator")
                        parse_key = False
                        continue
                    if parse_key == True:
                        key += char_
                    else:
                        value += char_
                    prev_char = char_
        else:
            for character in self.stream_obj:
                self.read_position += 1
                if self.read_position == len(self.stream_obj):
                    if key != "":
                        if parse_key == True and self.err_tolerance == False:
                            raise LookupError("Invalid entry detected near Line " + str(line) + ":"  + str(column))
                    self.done_reading()
                    break
                column += 1
                if character == '\n':
                    line += 1
                    column = 0
                if character == self.seperator and self.stream_obj[self.read_position-1] != '/' and not parse_key:
                    if key == "" and value =="":
                        continue
                    if parse_key == True and self.err_tolerance == False:
                        raise LookupError("Invalid entry detected near Line " + str(line) + ":"  + str(column))
                    break
                if character == self.delimeter and parse_key:
                    if value != "" and self.err_tolerance == False:
                        raise LookupError("The input is imporperly sepreated near Line " + str(line) + ":"  + str(column)+". Check the separator")
                    parse_key = False 
                    continue
                if parse_key:
                    key += character
                else:
                    value += character
            self.read_position += 1
        return (
                key.strip() if self.triming_key else key, 
                un_escape_string(value, self.seperator)
            )
        
    def done_reading(self):
        self.has_next_ = False
        self.done_reading_ = True






