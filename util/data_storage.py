import pickle, re

import util.ret as ret

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

#officially deprecated json functions
#If you want to use them, look in OneNote
#THEN CLOSE ONENOTE AND RECONSIDER YOUR ACTIONS
#YOU CAN HANDLE ALL OF THIS MUCH BETTER THROUGH PICKLE
#AND IF TRULY NECESSARY, IMPORT A GODDAMN LIBRARY