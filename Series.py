import ret, data_storage
from Character import Character

class Series:

    characters = []
    
    @staticmethod
    def import_object(object_file):
        return data_storage.load_pickle(object_file)

    def __init__(self, book_file, arc_file, char_file, object_file):
        self.populate_books(book_file)
        self.populate_arcs(arc_file)
        self.populate_characters(char_file)
        data_storage.dump_pickle(self, object_file)

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