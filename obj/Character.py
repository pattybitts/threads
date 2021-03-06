import util.ret as ret
import util.log as log

from obj.Scene import Scene
import obj.Universe as Universe

class Character:

    def __init__(self, name_str: str, uni=None, gender_str: str="", r_val: int=0, g_val: int=0, b_val: int=0):
        self.name  = str(name_str)
        self.gender = gender_str
        self.tier = ""
        self.color = {"r": r_val, "g": g_val, "b": b_val}
        self.aliases = []
        self.joins = []
        self.tags = []
        self.universe = uni
        #not yet. see notes
        #self.featured = []

    @staticmethod
    def match(characters, search_str: str, scene=None):
        characters = list(filter(lambda c: (isinstance(c, Character)), characters))
        if len(characters) <= 0: return ret.ERROR
        #first, matches all characters with this alias
        matches = []
        for c in characters:
            for a in c.aliases:
                if a[0] == search_str:
                    matches.append(c)
                    break
        if len(matches) == 1:
            return matches[0]
        elif len(matches) == 0:
            return ret.NOT_FOUND
        else:
            #next, checks to see if any character has been prioritized with an !alias
            priority_matches = []
            for m in matches:
                for a in m.aliases:
                    if a[0] == "!" + search_str:
                        priority_matches.append(m)
                        break
            if len(priority_matches) == 1:
                return priority_matches[0]
            elif len(priority_matches) > 1:
                return ret.ERROR
            else:
                #last, checks to see if only one character is included in the scene
                if scene is None: return ret.ERROR
                included_matches = []
                for m in matches:
                    for i in scene.included:
                        if m == i["character"]:
                            included_matches.append(m)
                            break
                if len(included_matches) == 1:
                    return included_matches[0]
                else:
                    return ret.ERROR

    def common_name(scene=None):
        #find character's series (later universe)
        #might methodize or variablize this later
        pass  

    def add_alias(self, alias: str, scene: Scene):
        self.aliases.append([alias, scene])

    def add_join(self, join, scene: Scene):
        if not isinstance(join, Character):
            return
        self.joins.append([join, scene])

    def add_tag(self, tag: str, scene: Scene):
        self.tags.append([tag, scene])

    def intro_scene(self):
        for a in self.aliases:
            if a[0] == self.name:
                return a[1]
        return ret.NOT_FOUND

    def print_info(self):
        alias_str = ""
        if len(self.aliases) > 0:
            alias_str += "\n<u>Aliases:</u>\n"
            for a in self.aliases:
                alias_str = alias_str + "  " + a[0] + ": " + a[1].name + "\n"
            alias_str = alias_str.rstrip()
        join_str = ""
        if len(self.joins) > 0:
            join_str += "\n<u>Joins:</u>\n"
            for j in self.joins:
                join_str = join_str + "  " + j[0].name + ": " + j[1].name + "\n"
            join_str = join_str.rstrip()
        tag_str = ""
        if len(self.tags) > 0:
            tag_str += "\n<u>Tags:</u>\n"
            for t in self.tags:
                tag_str = tag_str + "  " + t[0] + ": " + t[1].name + "\n"
            tag_str = tag_str.rstrip()
        color_str = "Color: R: " + str(self.color["r"])
        color_str = color_str + " G: " + str(self.color["g"])
        color_str = color_str + " B: " + str(self.color["b"])
        return "<b>(Character) " + self.name + "</b> from: " + self.universe.name + "\n" \
            + "Gender: " + self.gender + "\n" \
            + color_str + alias_str + join_str + tag_str + "\n"        

    #all methods below here are before the 1-19 object rebuild and are suspect
    
    def print_aliases(self):
        alias_str = ""
        for a in self.aliases:
            alias_str = alias_str + str(a) + "\n"
        return alias_str.rstrip()

    def print_tags(self):
        tag_str = ""
        for t in self.tags:
            tag_str = tag_str + str(t) + "\n"
        return tag_str.rstrip()

    def has_tag(self, tag_check: str):
        for t in self.tags:
            if str.lower(tag_check) == str.lower(t):
                return True
        return False
    
    def prominence_score(self, scene_group, series):
        from obj.Series import Series
        if not isinstance(series, Series):
            return ret.ERROR
        char_qwords = 0
        total_qwords = 0
        char_pwords = 0
        total_pwords = 0
        for sg in scene_group:
            if not isinstance(sg, Scene):
                continue
            for c in sg.characters:
                c_match = Character.match_character(series.characters, c["name"])
                if c_match != ret.ERROR and c_match.name == self.name:
                    char_qwords += c["quote_words"]
                total_qwords += c["quote_words"]
            p_match = Character.match_character(series.characters, sg.primary_character)
            if p_match != ret.ERROR and p_match.name == self.name:
                char_pwords += sg.wordcount
            total_pwords += sg.wordcount
        quote_score = 0 if total_qwords == 0 else char_qwords / total_qwords
        primary_score = 0 if total_pwords == 0 else char_pwords / total_pwords
        return .5 * (quote_score) + .5 * (primary_score)

    def apply_filter(self, sub: str, comp: str, obj: str):  
        if sub == "name":
            if comp == "==":
                return (obj == str.lower(self.name))
            elif comp == "!=":
                return (obj != str.lower(self.name))
            elif comp == ">=":
                return (Character.match_character([self], obj) != ret.ERROR)
            elif comp == "<=":
                return (Character.match_character([self], obj))
        elif sub == "tag":
            if comp == ">=":
                return self.has_tag(obj)
            elif comp == "<=":
                return not self.has_tag(obj)
        elif sub == "gender":
            if comp == "==":
                return (str.lower(self.gender) == obj)
            elif comp == "!=":
                return not (str.lower(self.gender) == obj)
        return ret.ERROR