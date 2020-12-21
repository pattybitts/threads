#from obj.Character import Character
from obj.ULocation import ULocation
from obj.UTime import UTime

class Scene:

    def __init__(self, name: str, firstword: int, wordcount: int, p_character: str, summary: str = ""):
        self.name = name
        self.firstword = firstword
        self.wordcount = wordcount
        self.locations = []
        self.time = UTime()
        self.p_character = p_character
        self.characters = []
        self.summary = summary

    def is_featured(self, character, series):
        for c in self.characters:
            c_match = Character.match_character(series.characters, c["name"])
            if c_match != ret.ERROR and c_match.name == character.name:
                return c["featured"]