import datetime

import util.ret as ret
import util.data_storage as ds

from obj.Universe import Universe

class Library:

    def __init__(self):
        self.universes = []
        self.last_updated = datetime.datetime.now()

    def save(self, dump_file):
        ds.dump_pickle(self, dump_file)

    @staticmethod
    def load(load_file):
        library = ds.load_pickle(load_file)
        if not ret.success(library):
            return ret.ERROR
        return library

    def get_universe(self, uni_name):
        universe = Universe.match(self.universes, uni_name)
        if not ret.success(universe):
            universe = Universe(uni_name)
            self.universes.append(universe)
        return universe

    def print_info(self):
        resp = "(Library) Created: " + self.last_updated.strftime("%m_%d_%y_%H%M")
        resp += "\nUniverses:\n"
        for u in self.universes:
            resp += u.name + "\n"
        return resp