import pickle, re

import util.ret as ret

#ooh boy, we have a massive object and front end rework ahead of us
#we need to shift the cmd in paradigm to take a save file
ACTIVE_FILE = "data\\wot_0"

def dump_pickle(object, filename):
    pfile = open(filename, 'wb')
    pickle.dump(object, pfile, pickle.DEFAULT_PROTOCOL)
    pfile.close()

def load_pickle(filename):
    try:
        pfile = open(filename, 'rb')
        object = pickle.load(pfile)
        pfile.close()
        return object
    except:
        return ret.ERROR

#to be archived or repurposed, not using json for this project
#TODO: I'm using these again for rudimentary save files, but that just highlights that I NEED to
#rework this whole mess
#given a section of json text and a target term, returns an array of the values it is keyed to
def create_array(array_text, target):
    out_array = []
    cut = cut_unit(array_text, array_text.find("\"" + target + "\""))
    if cut == ret.ERROR or cut[0] != target:
        return ret.ERROR
    cut_text = cut[1]
    next_bracket = find_next_bracket(cut_text)
    if next_bracket == ret.ERROR:
        return ret.ERROR
    elif next_bracket == '{' or next_bracket == '\"':
        cut = cut_unit(cut_text, cut_text.find(next_bracket))
        out_array.append(cut[0])
    elif next_bracket == '[':
        next_bracket = find_next_bracket(cut_text[cut_text.find(next_bracket)+1:])
        i = 0
        while next_bracket != ']' and next_bracket != ret.ERROR:
            cut = cut_unit(cut_text, cut_text.find(next_bracket))
            out_array.append(cut[0])
            cut_text = cut[1]
            next_bracket = find_next_bracket(cut_text)
            i += 1
    if len(out_array) < 1:
        return ret.ERROR
    return out_array

#to be archived or repurposed, not using json for this project
#given a string and a start point of quotes or parentheses, returns the unit of text contained within
def cut_unit(full_string, start):
    if start < 0:
        return ret.ERROR
    open = full_string[start]
    if open == '{':
        close = '}'
    elif open == '[':
        close = ']'
    elif open == '(':
        close = ')'
    elif open == "\"":
        close = "\""
    else:
        return ret.ERROR

    balance = 1
    for i in range(start + 1, len(full_string) - 1):
        if full_string[i] == close:
            balance -= 1
        elif full_string[i] == open:
            balance += 1
        if balance == 0:
            end = i
            break
    if balance > 0:
        return ret.ERROR
    return [full_string[start+1:end], full_string[end+1:]]

#see above
def find_next_bracket(text):
    for char in text:
        if char == '\"' \
            or char == '{' or char == '}' \
            or char == '[' or char == ']':
            return char
    return ret.ERROR

#given a term and a replacement value, finds the unit and replaces it in the string
def replace_unit(full_string, term, replacement):
    new_string = re.sub("\"" + term + "\":\s\"(.*)\"", "\"" + term + "\": " + replacement, full_string)
    if new_string != full_string:
        return new_string
    else:
        return ret.NOT_FOUND