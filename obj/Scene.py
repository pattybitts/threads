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
        self.perspectives = []
        self.locations = []
        self.included = []

    def add_perspective(self, new_perspective: Character):
        self.perspectives.append(new_perspective)

    def get_location(self, loc_name: str):
        for l in self.locations:
            if l.name == loc_name:
                return l
        return ret.ERROR

    def add_location(self, new_loc: Location):
        self.locations.append(new_loc)

    def print_info(self):
        out = "<b>(Scene) " + self.name + "</b>\n"
        per_str = ""
        for p in self.perspectives:
            per_str += p.name + ", "
        per_str = per_str.rstrip(", ")
        #NOTE: not using locations until universe update
        loc_str = ""
        for l in self.locations:
            loc_str += l.name + ", "
        loc_str = loc_str.rstrip(", ")
        out += "Perspectives: " + per_str + "; Words: " + str(self.wordcount) + "\n"
        out += "Description: " + self.description + "\n"
        featured_char_strs = []
        mentioned_char_strs = []
        for i in self.included:
            inc_str = ""
            character = i["character"]
            new_str = "(New) " if ret.success(character.intro_scene()) and character.intro_scene() == self else ""
            inc_str += new_str + character.name + "; Words: " + str(i["quotes"]) + ", Calls: " + str(i["mentions"]) + "\n"
            for a in character.aliases:
                if a[1] == self:
                    inc_str += "--New Alias: " + a[0] + "\n"
            for j in character.joins:
                if j[1] == self:
                    inc_str += "--New Join: " + j[0].name + "\n"
            for t in character.tags:
                if t[1] == self:
                    inc_str += "--New Tag: " + t[0] + "\n"
            if i["featured"]:
                featured_char_strs.append(inc_str)
            else:
                mentioned_char_strs.append(inc_str)
        if len(featured_char_strs) > 0:
            out += "<u>Featured:</u>\n"
            for fcs in featured_char_strs:
                out += fcs
        if len(mentioned_char_strs) > 0:
            out += "<u>Mentioned:</u>\n"
            for mcs in mentioned_char_strs:
                out += mcs
        return out

    #all methods below here are before the 1-19 object rework

    def is_featured(self, character, series):
        return
        for c in self.characters:
            c_match = Character.match_character(series.characters, c["name"])
            if c_match != ret.ERROR and c_match.name == character.name:
                return c["featured"]