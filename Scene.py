#from Character import Character
from Location import Location
from UTime import UTime

class Scene:

    def __init__(self, name: str, firstword: int, wordcount: int, p_character: str):
        self.name = name
        self.firstword = firstword
        self.wordcount = wordcount
        self.locations = []
        self.time = UTime()
        self.p_character = p_character
        self.characters = []