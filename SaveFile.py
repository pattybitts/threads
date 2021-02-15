import util.data_storage as ds
import util.ret as ret

class SaveFile:

    def __init__(self, name="", book_file="", library_file="", universe_name="", series_name="", book_name="", page_start=0):
        self.name  = name
        self.book_file = book_file
        self.library_file = library_file
        self.universe_name = universe_name
        self.series_name = series_name
        self.book_name = book_name
        self.page_start = page_start

    def save(self, save_str=""):
        if save_str == "": save_str = self.name
        ds.dump_pickle(self, save_str)

    @staticmethod
    def load(load_file):
        save_file = ds.load_pickle(load_file)
        if not ret.success(save_file):
            return ret.ERROR
        return save_file

    def print_info(self):
        resp = "Name: " + self.name + "\n"
        resp += "Book File: " + self.book_file + "\n"
        resp += "Library File: " + self.library_file + "\n"
        resp += "Universe Name: " + self.universe_name + "\n"
        resp += "Series Name: " + self.series_name + "\n"
        resp += "Book Name: " + self.book_name + "\n"
        resp += "Page Start: " + str(self.page_start)
        return resp    