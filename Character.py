import data_storage, log

class Character:

    def __init__(self, char_string):
        self.name = data_storage.create_array(char_string, "Name")[0]
        self.aliases = data_storage.create_array(char_string, "Aliases")
        self.gender = data_storage.create_array(char_string, "Gender")[0]
        self.allegiance = data_storage.create_array(char_string, "Allegiance")[0]
        self.tier = data_storage.create_array(char_string, "Tier")[0]
        self.color = {}
        self.color[0] = 0#data_storage.create_array(data_storage.create_array(char_string, "Color"), "R")[0]
        self.color[1] = 1#data_storage.create_array(data_storage.create_array(char_string, "Color"), "G")[1]
        self.color[2] = 2#data_storage.create_array(data_storage.create_array(char_string, "Color"), "B")[2]
        self.tags = data_storage.create_array(char_string, "Tags")

    def print_info(self):
        alias_str = ""
        for a in self.aliases:
            alias_str = alias_str + "  " + str(a) + "\n"
        alias_str = alias_str.rstrip()
        tag_str = ""
        for t in self.tags:
            tag_str = tag_str + "  " + str(t) + "\n"
        tag_str = tag_str.rstrip()
        color_str = "  R: " + str(self.color[0]) + "\n"
        color_str = color_str + "  G: " + str(self.color[1]) + "\n"
        color_str = color_str + "  B: " + str(self.color[2])
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
