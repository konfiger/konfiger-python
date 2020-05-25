
def escape_string(value, *extra_escape):
    final_value = ""
    for i in range(0, len(value)):
        c = value[i]
        if len(extra_escape) > 0:
            for extra in extra_escape:
                if c == extra:
                    final_value += "/"
                    break
        final_value += c
    return final_value
    
def un_escape_string(value, *extra_escape):
    final_value = ""
    for i in range(0, len(value)):
        c = value[i]
        if c == '/':
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
            final_value += "/" + value[d]
            continue
        final_value += c
    return final_value
