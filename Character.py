import data_storage, log

class Character:

    def __init__(self, char_string):
        self.name = data_storage.create_array(char_string, "Name")[0]
        self.aliases = data_storage.create_array(char_string, "Aliases")
        self.gender = data_storage.create_array(char_string, "Gender")[0]
        self.allegiance = data_storage.create_array(char_string, "Allegiance")[0]
        self.tier = data_storage.create_array(char_string, "Tier")[0]
        self.color = data_storage.create_array(char_string, "Color")
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
        return self.name + "\n" \
            + "Aliases:\n" + alias_str + "\n" \
            + "Gender: " + self.gender + "\n" \
            + "Allegiance: " + self.allegiance + "\n" \
            + "Tier: " + self.tier + "\n" \
            + "Tags:\n" + tag_str
    
    def print_aliases(self):
        alias_str = ""
        for a in self.aliases:
            alias_str = alias_str + str(a) + "\n"
        return alias_str.rstrip()


