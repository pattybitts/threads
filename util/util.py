import re

import util.log as log

def is_number(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False

def split(input_str: str, sep: str="\\s+", flags: int=0):
    str_trim = input_str.strip()
    if str_trim == "": return []
    split_arr = re.split(sep + "(?!$)", str_trim, flags)
    trim_arr = []
    for sa in split_arr:
        sa = sa.strip()
        trim_arr.append(sa)
    return trim_arr
    
def join(input_arr, joiner: str=","):
    if len(input_arr) < 1:
        return ""
    return joiner.join(input_arr)