#Generic Errors
SUCCESS = 0
ERROR = -1
BAD_INPUT = -2
NOT_FOUND = -3 #as in, not found in search. not fatal in match
DUPLICATE = -4 #the action or creation attempted already exists

#Website Directions
HOME = 1
ADD_CHAR = 2
EDIT_CHAR = 3
GRAPH_TOOL = 4
TEXT_TOOL = 5

def success(ret):
    if ret is None: return False
    if not isinstance(ret, int): return True
    return ret >= 0