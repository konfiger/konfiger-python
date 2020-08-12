
"""
    The MIT License
    Copyright 2020 Adewale Azeez <azeezadewale98@gmail.com>.
"""

def type_of(arg):
    return 

def is_string(arg):
    return isinstance(arg, str)

def is_int(arg):
    return isinstance(arg, int)

def is_number(arg):
    return is_int(arg)

def is_char(arg):
    return isinstance(arg, str) and len(arg) == 1

def is_bool(arg):
    return isinstance(arg, bool)

def is_float(arg):
    return isinstance(arg, float)

def is_object(arg):
    return isinstance(arg, type)

def escape_string(value, *extra_escape):
    final_value = ""
    for i in range(0, len(value)):
        c = value[i]
        if len(extra_escape) > 0:
            for extra in extra_escape:
                if c == extra:
                    final_value += "^"
                    break
        final_value += c
    return final_value
    
def un_escape_string(value, *extra_escape):
    final_value = ""
    for i in range(0, len(value)):
        c = value[i]
        if c == '^':
            if i == len(value) - 1:
                final_value += c
                break
            i = i + 1
            d = i
            if len(extra_escape) > 0:
                continua = False
                for extra in extra_escape:
                    if value[d] == extra:
                        continua = True
                        break
                if continua:
                    continue
            final_value += "^" + value[d]
            continue
        final_value += c
    return final_value
