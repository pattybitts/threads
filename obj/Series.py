import util.ret as ret
import util.data_storage as ds

from obj.Character import Character
from obj.Book import Book
from obj.Arc import Arc

class Series:

    def __init__(self, name:str):
        self.characters = []
        self.books = []
        self.arcs = []
        self.name = name

    #all methods below here are from before the 1-19 obj rework and are therefore suspect

    def replace_char(self, new_char, base_name):
        for c in self.characters:
            if c.name == base_name:
                self.characters.remove(c)
                self.characters.append(new_char)
                self.characters.sort(key=self.char_place)
                return ret.SUCCESS
        return ret.ERROR

    def add_char(self, new_char):
        if Character.match_character(self.characters, new_char.name, True) != ret.ERROR:
            return ret.ERROR
        self.characters.append(new_char)
        self.characters.sort(key=self.char_place)
        return ret.SUCCESS

    def char_place(self, c: Character):
        scene_group = []
        for b in self.books:
            for s in b.scenes:
                scene_group.append(s)
        return -c.prominence_score(scene_group, self), self.first_featured(c), c.name

    def first_featured(self, c: Character):
        s_count = 0
        for b in self.books:
            for s in b.scenes:
                s_count += 1
                if s.is_featured(c, self):
                    return s_count
        return -1

    def add_book(self, new_book: Book):
        self.books.append(new_book)

    def add_arc(self, new_arc: Arc):
        self.arcs.append(new_arc)