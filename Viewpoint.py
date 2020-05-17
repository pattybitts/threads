class Viewpoint:

    def __init__(self, num, primary, words):
        self.number = num
        self.wordcount = words
        self.primary_character = primary
        self.featured = []

    def add_featured(self, new_char):
        self.featured.append(new_char)

    def print_viewpoint(self):
        out = "Primary: " + self.primary_character.name + "\n"
        out += "Wordcount: " + str(self.wordcount) + "\n"
        out += "Featured: "
        for f in self.featured:
            out += f.name + ", "
        return out.rstrip(", ")

