import util.ret as ret

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
        return "(Chapter) " + self.name + " (" + str(self.placement) + "):\n" \
            + "Contains (" + str(len(self.scenes)) + ") Scenes\n"