import datetime

import util.ret as ret
import util.data_storage as ds

from obj.Series import Series

class Library:

    def __init__(self):
        self.series = []
        self.last_updated = datetime.datetime.now()

    def save(self, dump_file):
        ds.dump_pickle(self, dump_file)

    @staticmethod
    def load(load_file):
        library = ds.load_pickle(load_file)
        if not ret.success(library):
            return ret.ERROR
        return library

    def add_series(self, new_series: Series):
        self.series.append(new_series)

    def get_series(self, series_name: str):
        for s in self.series:
            if s.name == series_name:
                return s
        return ret.NOT_FOUND

    def get_info(self):
        resp = "Created: " + self.last_updated.strftime("%m_%d_%y_%H%M")
        resp += "\nSeries:\n"
        for s in self.series:
            resp += s.name + "\n"
        return resp