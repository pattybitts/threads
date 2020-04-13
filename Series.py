import ret, data_storage, log
from Character import Character

class Series:

    def __init__(self):
        self.characters = []
    
    def save(self, dump_file):
        data_storage.dump_pickle(self, dump_file)

    def find_char(self, input_text, strict=False):
        for c in self.characters:
            if c.name == input_text:
                return c
        return ret.ERROR

    def replace_char(self, new_char):
        for c in self.characters:
            if c.name == new_char.name:
                self.characters.remove(c)
                self.characters.append(new_char)
                return ret.SUCCESS
        return ret.ERROR

    def add_char(self, new_char):
        if self.find_char(new_char.name, True) != ret.ERROR:
            return ret.ERROR
        self.characters.append(new_char)
        return ret.SUCCESS