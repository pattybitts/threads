from obj.Scene import Scene

class Chapter:

    def __init__(self, title, num):
        self.name = title
        self.placement = num
        self.scenes = []

    def add_scene(self, new_scene: Scene):
        self.scenes.append(new_scene)

    def print_info(self):
        return "(Chapter) " + self.name + " (" + str(self.placement) + "):\n" \
            + "Contains (" + str(len(self.scenes)) + ") Scenes"