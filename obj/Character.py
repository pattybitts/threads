import util.ret as ret

class Character:

    def __init__(self, name_str, alias_str, gender_str, r_val, g_val, b_val, tag_str):
        self.name  = name_str
        self.aliases = []
        aliases = alias_str.split("\n")
        for a in aliases:
            a = a.strip("\n\r ")
            self.aliases.append(a)
        self.gender = gender_str
        self.color = {"r": r_val, "g": g_val, "b": b_val}
        self.tags = []
        tags = tag_str.split("\n")
        for t in tags:
            t = t.strip("\n\r ")
            self.tags.append(t)
        self.joined_characters = []

    def print_info(self):
        alias_str = ""
        for a in self.aliases:
            alias_str = alias_str + "  " + str(a) + "\n"
        alias_str = alias_str.rstrip()
        tag_str = ""
        for t in self.tags:
            tag_str = tag_str + "  " + str(t) + "\n"
        tag_str = tag_str.rstrip()
        color_str = "  R: " + str(self.color["r"]) + "\n"
        color_str = color_str + "  G: " + str(self.color["g"]) + "\n"
        color_str = color_str + "  B: " + str(self.color["b"])
        return "(Character) " + self.name + "\n" \
            + "Aliases:\n" + alias_str + "\n" \
            + "Gender: " + self.gender + "\n" \
            + "Tags:\n" + tag_str + "\n" \
            + "Color:\n" + color_str
    
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

    @staticmethod
    def match_character(list, name: str, strict=False):
        best_match = ret.ERROR
        best_score = 0
        for c in list:
            if not isinstance(c, Character):
                continue
            if c.name == name:
                return c
            if not strict:
                alias_tags = c.print_aliases().split()
                name_tags = c.name.split()
                for n in name_tags:
                    alias_tags.append(n)
                name_terms = name.split()
                score = 0
                for i in name_terms:
                    for a in alias_tags:
                        if i.lower() == a.lower():
                            score += 1
                if score > best_score:
                    best_match = c
                    best_score = score
        return best_match
    
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
                return (Character.match_character([self], obj) == ret.ERROR)
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