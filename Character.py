import data_storage, log, ret

class Character:

    def __init__(self, name_str, alias_str, gender_str, tier_str, r, g, b, tag_str):
        self.name  = name_str
        self.aliases = alias_str.split("\n")
        self.gender = gender_str
        self.tier = tier_str
        self.color = {}
        self.color["r"] = r
        self.color["g"] = g
        self.color["b"] = b
        self.tags = tag_str.split("\n")

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
        return self.name + "\n" \
            + "Aliases:\n" + alias_str + "\n" \
            + "Gender: " + self.gender + "\n" \
            + "Tier: " + self.tier + "\n" \
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

    def tier_value(self):
        key = {
            "S": 5,
            "A": 4,
            "B": 3,
            "C": 2,
            "D": 1,
            "F": 0
            }
        return key.get(self.tier, 0)

    @staticmethod
    def match_character(list, name: str, strict=False):
        best_match = ret.ERROR
        best_score = 0
        for c in list:
            if isinstance(c, Character()):
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
                    elif score == best_score and best_match != ret.ERROR:
                        if c.tier_value() > best_match.tier_value():
                            best_match = c
        return best_match        