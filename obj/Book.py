from obj.Chapter import Chapter
from obj.Scene import Scene
from obj.Milestone import Milestone

class Book:

    def __init__(self, title: str, num: int):
        self.name = title
        self.placement = num
        self.chapters = []
        self.milestones = []

    def add_chapter(self, new_chapter: Chapter):
        self.chapters.append(new_chapter)
        
    def add_scene(self, new_scene: Scene):
        self.scenes.append(new_scene)
        
    def add_milestone(self, new_milestone: Milestone):
        self.milestones.append(new_milestone)