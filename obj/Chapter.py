from obj.Scene import Scene

class Chapter:

    def __init__(self, title, num):
        self.name = title
        self.placement = num
        self.scenes = []

    def add_scene(self, new_scene: Scene):
        self.scenes.append(new_scene)

    #all methods below are before 1-19

    def print_chapter(self):
        out = "(Chapter) " + self.title + " (" + str(self.number) + "):\n"
        return out