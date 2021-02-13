import util.ret as ret
import util.util as util

from obj.Scene import Scene

class Chapter:

    def __init__(self, title, num):
        self.name = title
        self.placement = num
        self.scenes = []

    def add_scene(self, new_scene: Scene):
        for s in self.scenes:
            if s.wordcount == new_scene.wordcount and s.description == new_scene.description:
                return ret.DUPLICATE
        self.scenes.append(new_scene)
        return ret.SUCCESS    

    def print_info(self):
        return "<b>(Chapter) " + self.name + " (" + str(self.placement) + "):</b>\n" \
            + "Contains (" + str(len(self.scenes)) + ") Scenes\n"
    
    @staticmethod
    def match(chapters, match_str: str, exact_match=True):
        chapters = list(filter(lambda c: (isinstance(c, Chapter)), chapters))
        if len(chapters) <= 0: return ret.ERROR
        for c in chapters:
            if c.name == match_str: return c
        if exact_match: return ret.NOT_FOUND
        best_score = 100
        best_match = ret.NOT_FOUND
        for c in chapters:
            score = 0
            c_parts = util.split(c.name)
            match_parts = util.split(match_str)
            for cp in c_parts:
                for mp in match_parts:
                    if cp == mp: score += 100
            score += c.placement
            if score >= best_score: best_match = c
        return best_match