#Generic Errors
SUCCESS = 0
ERROR = -1
INVALID_INPUT = -2
NOT_FOUND = -3 #as in, not found in search. not fatal in match

#Website Directions
HOME = 1
ADD_CHAR = 2
EDIT_CHAR = 3
GRAPH_TOOL = 4
TEXT_TOOL = 5

def success(ret):
    return ret >= 0