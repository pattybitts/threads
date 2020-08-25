#from Character import Character
from ULocation import ULocation
from UTime import UTime

class Scene:

    def __init__(self, name: str, firstword: int, wordcount: int, p_character: str):
        self.name = name
        self.firstword = firstword
        self.wordcount = wordcount
        self.locations = []
        self.time = UTime()
        self.p_character = p_character
        self.characters = []

    def is_featured(self, character, series):
        for c in self.characters:
            c_match = Character.match_character(series.characters, c["name"])
            if c_match != ret.ERROR and c_match.name == character.name:
                return c["featured"]