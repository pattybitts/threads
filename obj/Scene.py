import util.ret as ret

import obj.Character as Character
from obj.Location import Location
#from obj.UTime import UTime

class Scene:

    def __init__(self, name: str, num: int, wordcount: int, p_character: Character, description: str = ""):
        self.name = name
        self.placement = num
        self.wordcount = wordcount
        self.primary = p_character
        self.description = description
        self.locations = []
        self.included = []

    def get_location(self, loc_name: str):
        for l in self.locations:
            if l.name == loc_name:
                return l
        return ret.ERROR

    def add_location(self, new_loc: Location):
        self.locations.append(new_loc)

    #all methods below here are before the 1-19 object rework

    def is_featured(self, character, series):
        return
        for c in self.characters:
            c_match = Character.match_character(series.characters, c["name"])
            if c_match != ret.ERROR and c_match.name == character.name:
                return c["featured"]