import ret, data_storage, log
from Character import Character

class Series:

    def __init__(self, book_file, arc_file, char_file, dump_file):
        self.populate_books(book_file)
        self.populate_arcs(arc_file)
        self.characters = []
        self.populate_characters(char_file)
        data_storage.dump_pickle(self, dump_file)

    def populate_characters(self, char_file):
        with open(char_file) as file:
            full_text = file.read()
            character_texts = data_storage.create_array(full_text, "Characters")
            for ct in character_texts:
                new_character = Character(ct)
                self.characters.append(new_character)

    def populate_books(self, book_file):
        return ret.SUCCESS

    def populate_arcs(self, arc_file):
        return ret.SUCCESS

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