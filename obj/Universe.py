import util.ret as ret
import util.util as util

from obj.Series import Series
from obj.Character import Character
from obj.Location import Location
from obj.Scene import Scene

class Universe:

    def __init__(self, uni_name: str):
        self.name = uni_name
        self.series = []
        self.locations = []
        self.characters = []

    @staticmethod
    def match(universes, match_str: str, exact_match=True):
        universes = list(filter(lambda u: (isinstance(u, Universe)), universes))
        if len(universes) <= 0: return ret.ERROR
        for u in universes:
            if u.name == match_str: return u
        if exact_match: return ret.NOT_FOUND
        best_score = 1
        best_match = ret.NOT_FOUND
        for u in universes:
            score = 0
            u_parts = util.split(u.name)
            match_parts = util.split(match_str)
            for up in u_parts:
                for mp in match_parts:
                    if up == mp: score += 1
            if score >= best_score: best_match = u
        return best_match

    def get_series(self, se_name):
        series = Series.match(self.series, se_name)
        if not ret.success(series):
            series = Series(se_name, len(self.series)+1)
            self.series.append(series)
        return series

    def get_character(self, ch_name, scene):
        character = Character.match(self.characters, ch_name, scene)
        return character
        if character == ret.ERROR:
            return ret.ERROR
        if character == ret.NOT_FOUND:
            character = Character(ch_name)
            character.add_alias(ch_name, scene)
            self.add_character(character)
        return character
            
    #TODO
    #def get_location(self, loc_name)

    def print_info(self):
        s_str = ""
        for s in self.series:
            s_str += "  " + str(s.placement) + ": " + s.name + ": " + str(len(s.books)) + " books\n"
        s_str = s_str.rstrip()
        return "(Universe) " + self.name + ":\n" \
            + "Contains (" + str(len(self.characters)) + ") Characters\n" \
            + "Contains (" + str(len(self.series)) + ") Series:\n" \
            + s_str + "\n"