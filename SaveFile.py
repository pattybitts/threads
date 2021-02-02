import util.data_storage as ds
import util.ret as ret

class SaveFile:

    def __init__(self, name="", book_file="", library_file="", series_name="", book_name="", position=0):
        self.name  = name
        self.book_file = book_file
        self.library_file = library_file
        self.series_name = series_name
        self.book_name = book_name
        self.position = position

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
        resp += "Series Name: " + self.series_name + "\n"
        resp += "Book Name: " + self.book_name + "\n"
        resp += "Position: " + str(self.position)
        return resp    