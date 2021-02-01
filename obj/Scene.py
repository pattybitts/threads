import util.ret as ret

import obj.Character as Character
from obj.Location import Location
#from obj.UTime import UTime

class Scene:

    def __init__(self, name: str, num: int, wordcount: int, description: str = ""):
        self.name = name
        self.placement = num
        self.wordcount = wordcount
        self.description = description
        self.primary = None
        self.locations = []
        self.included = []

    def set_primary(self, p_character: Character):
        self.primary = p_character

    def get_location(self, loc_name: str):
        for l in self.locations:
            if l.name == loc_name:
                return l
        return ret.ERROR

    def add_location(self, new_loc: Location):
        self.locations.append(new_loc)

    def print_info(self):
        loc_str = ""
        for l in self.locations:
            loc_str += l.name + ", "
        loc_str  = loc_str.rstrip(", ")
        inc_str = ""
        for i in self.included:
            character = i["character"]
            featured_str = "Featured" if i["featured"] else "Mentioned"
            inc_str += "  " + character.name + " (" + featured_str + ", Words: " + str(i["quotes"]) + ", Calls: " + str(i["mentions"]) + ")\n"
            for a in character.aliases:
                if a[1] == self:
                    inc_str += "  New Alias: " + a[0] + "\n"
            for j in character.joins:
                if j[1] == self:
                    inc_str += "  New Join: " + j[0].name + "\n"
            for t in character.tags:
                if t[1] == self:
                    inc_str += "  New Tag: " + t[0] + "\n"
            inc_str += "\n"
        return "(Scene) " + self.name + "\n" \
            + "Perspective: " + self.primary.name + "; Words: " + str(self.wordcount) + "\n" \
            + "Locations: " + loc_str + "\n" \
            + "Description: " + self.description + "\n" \
            + "Included Characters:\n" + inc_str

    #all methods below here are before the 1-19 object rework

    def is_featured(self, character, series):
        return
        for c in self.characters:
            c_match = Character.match_character(series.characters, c["name"])
            if c_match != ret.ERROR and c_match.name == character.name:
                return c["featured"]