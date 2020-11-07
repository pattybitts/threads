from obj.Checkpoint import Checkpoint
from obj.Scene import Scene

class Arc:

    def __init__(self, name: str, climax: Checkpoint, protagonist: str):
        self.name = name
        self.protagonist = protagonist
        #self.supports = []
        self.climax = climax
        self.checkpoints = []
        self.scenes = []
