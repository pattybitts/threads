class Series:
    books = []
    arcs = []
    characters = []

    def __init__(self, char_file):
        self.populate_characters(char_file)

    def populate_characters(self, json_file):
        with open(json_file) as file:
            full_text = file.read()
        

            
