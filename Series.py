import ret, data_storage, log
from Character import Character

class Series:

    def __init__(self):
        self.characters = []
        self.books = []
    
    def save(self, dump_file):
        data_storage.dump_pickle(self, dump_file)

    def replace_char(self, new_char, base_name):
        for c in self.characters:
            if c.name == base_name:
                self.characters.remove(c)
                self.characters.append(new_char)
                return ret.SUCCESS
        return ret.ERROR

    def add_char(self, new_char):
        if self.find_char(new_char.name, True) != ret.ERROR:
            return ret.ERROR
        self.characters.append(new_char)
        return ret.SUCCESS

    def add_book(self, new_book):
        self.books.append(new_book)