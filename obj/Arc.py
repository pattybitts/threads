from Checkpoint import Checkpoint
from Scene import Scene

class Arc:

    def __init__(self, name: str, climax: Checkpoint, protagonist: str):
        self.name = name
        self.protagonist = protagonist
        #self.supports = []
        self.climax = climax
        self.checkpoints = []
        self.scenes = []
