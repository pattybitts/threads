import util.ret as ret

from obj.Chapter import Chapter
from obj.Milestone import Milestone

class Book:

    def __init__(self, title: str, num: int):
        self.name = title
        self.placement = num
        self.chapters = []
        self.milestones = []

    def find_chapter(self, ch_name: str):
        for c in self.chapters:
            if c.name == ch_name: return c
        ch_name_parts = ch_name.lower().split(" ")
        for cn in ch_name_parts:
            for c in self.chapters:
                c_parts = c.name.lower().split(" ")
                for cp in c_parts:
                    if cn == cp: return c
        return ret.ERROR

    def add_chapter(self, new_chapter: Chapter):
        self.chapters.append(new_chapter)
        
    def add_milestone(self, new_milestone: Milestone):
        self.milestones.append(new_milestone)