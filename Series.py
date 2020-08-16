import ret, data_storage, log
from Character import Character
from Book import Book
from Arc import Arc

class Series:

    def __init__(self, name:str):
        self.characters = []
        self.books = []
        self.arcs = []
        self.name = name
    
    def save(self, dump_file):
        data_storage.dump_pickle(self, dump_file)

    def replace_char(self, new_char, base_name):
        for c in self.characters:
            if c.name == base_name:
                self.characters.remove(c)
                self.characters.append(new_char)
                self.characters.sort(key=self.char_place)
                return ret.SUCCESS
        return ret.ERROR

    def add_char(self, new_char):
        if self.find_char(new_char.name, True) != ret.ERROR:
            return ret.ERROR
        self.characters.append(new_char)
        self.characters.sort(key=self.char_place)
        return ret.SUCCESS

    def char_place(self, c: Character):
        return -Character.tier_value(c.tier), self.first_featured(c), c.name

    def first_featured(self, c: Character):
        vp_count = 0
        for b in self.books:
            for ch in b.chapters:
                for v in ch.viewpoints:
                    vp_count += 1
                    if v.is_featured(c.name):
                        return vp_count
        return -1

    def add_book(self, new_book: Book):
        self.books.append(new_book)

    def add_arc(self, new_arc: Arc):
        self.arcs.append(new_arc)