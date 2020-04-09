import data_storage, log

class Character:

    def __init__(self, name_str, alias_str, gender_str, all_str, tier_str, r, g, b, tag_str):
        self.name  = name_str
        self.aliases = alias_str.split("\n")
        self.gender = gender_str
        self.allegiance = all_str
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
            + "Allegiance: " + self.allegiance + "\n" \
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
