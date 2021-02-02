import re

def is_number(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False

def split(input_str: str, sep: str="\\s+", flags: int=0):
    str_trim = input_str.strip()
    if str_trim == "": return []
    return re.split(sep + "(?!$)", str_trim, flags)
    
def join(input_arr, joiner: str=","):
    if len(input_arr) < 1:
        return ""
    return joiner.join(input_arr)