from obj.Scene import Scene

class Checkpoint:

    def __init__(self, name: str, description: str, scene: Scene):
        self.name = name
        self.placement = 0
        self.description = description
        self.scene = scene

    def info_str(self):
        return "goob"