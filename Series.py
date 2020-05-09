import ret, data_storage, log
from Character import Character

class Series:

    def __init__(self):
        self.characters = []
    
    def save(self, dump_file):
        data_storage.dump_pickle(self, dump_file)

    def find_char(self, input_text, strict=False):
        if strict:
            for c in self.characters:
                if c.name == input_text:
                    return c
            return ret.ERROR
        else:
            best_match = ret.ERROR
            best_score = 0
            for c in self.characters:
                if c.name == input_text:
                    return c
                alias_tags = c.print_aliases().split()
                name_tags = c.name.split()
                for n in name_tags:
                    alias_tags.append(n)
                input_terms = input_text.split()
                score = 0
                for i in input_terms:
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

    def replace_char(self, new_char, base_name):
        for c in self.characters:
            if c.name == base_name:
                self.characters.remove(c)
                self.characters.append(new_char)
                return ret.SUCCESS
        return ret.ERROR

    def add_char(self, new_char):
        if self.find_char(new_char.name, True) != ret.ERROR:
            return ret.ERROR
        self.characters.append(new_char)
        return ret.SUCCESS