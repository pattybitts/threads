import util.ret as ret
import util.data_storage as ds
import util.log as log

from obj.Character import Character
from obj.Book import Book
from obj.Arc import Arc
from obj.Scene import Scene

class Series:

    def __init__(self, name: str, num: int):
        self.characters = []
        self.books = []
        self.arcs = []
        self.name = name
        self.placement = num

    @staticmethod
    def match(series, match_str: str, exact_match=True):
        series = list(filter(lambda s: (isinstance(s, Series)), series))
        if len(series) <= 0: return ret.ERROR
        for s in series:
            if s.name == match_str: return s
        if exact_match: return ret.NOT_FOUND
        best_score = 1
        best_match = ret.NOT_FOUND
        for s in series:
            score = 0
            s_parts = util.split(s.name)
            match_parts = util.split(match_str)
            for sp in s_parts:
                for mp in match_parts:
                    if sp == mp: score += 1
            if score >= best_score: best_match = s
        return best_match

    def add_book(self, new_book: Book):
        self.books.append(new_book)

    def add_arc(self, new_arc: Arc):
        self.arcs.append(new_arc)

    def add_character(self, new_char: Character): 
        self.characters.append(new_char)

    def get_book(self, bo_name):
        book = Book.match(self.books, bo_name)
        if not ret.success(book):
            book = Book(bo_name, len(self.books)+1)
            self.books.append(book)
        return book

    def get_character(self, ch_name, scene):
        character = Character.match(self.characters, ch_name, scene)
        if character == ret.ERROR:
            return ret.ERROR
        if character == ret.NOT_FOUND:
            character = Character(ch_name)
            character.add_alias(ch_name, scene)
            self.add_character(character)
        return character

    def print_info(self):
        bo_str = ""
        for b in self.books:
            bo_str += "  " + str(b.placement) + ": " + b.name + ": " + str(len(b.chapters)) + " chapters\n"
        bo_str = bo_str.rstrip()
        return "(Series) " + self.name + " (" + str(self.placement) + "):\n" \
            + "Contains (" + str(len(self.books)) + ") Books:\n" \
            + bo_str + "\n" 

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
            return False
        self.characters.append(new_char)
        self.characters.sort(key=self.char_place)
        return True

    def char_place(self, c: Character):
        scene_group = []
        for b in self.books:
            for c in b.chapters:
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