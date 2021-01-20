from obj.Checkpoint import Checkpoint
from obj.Scene import Scene
from obj.Character import Character

class Arc:

    def __init__(self, name: str, climax: Checkpoint, protagonist: Character):
        self.name = name
        self.protagonist = protagonist
        self.climax = climax
        self.antagonists = []
        self.checkpoints = []
        self.scenes = []