import util.ret as ret

from obj.Chapter import Chapter
from obj.Milestone import Milestone

class Book:

    def __init__(self, title: str, num: int):
        self.name = title
        self.placement = num
        self.chapters = []
        self.milestones = []

    def get_chapter(self, ch_name):
        chapter = Chapter.match(self.chapters, ch_name)
        if not ret.success(chapter):
            chapter = Chapter(ch_name, len(self.chapters)+1)
            self.chapters.append(chapter)
        return chapter

    def add_chapter(self, new_chapter: Chapter):
        self.chapters.append(new_chapter)
        
    def add_milestone(self, new_milestone: Milestone):
        self.milestones.append(new_milestone)

    @staticmethod
    def match(books, match_str: str, exact_match=True):
        books = list(filter(lambda b: (isinstance(b, Book)), books))
        if len(books) <= 0: return ret.ERROR
        for b in books:
            if b.name == match_str: return b
        if exact_match: return ret.NOT_FOUND
        best_score = 100
        best_match = ret.NOT_FOUND
        for b in books:
            score = 0
            b_parts = util.split(b.name)
            match_parts = util.split(match_str)
            for bp in b_parts:
                for mp in match_parts:
                    if bp == mp: score += 100
            score += b.placement
            if score >= best_score: best_match = b
        return best_match

    def print_info(self):
        ch_str = ""
        for c in self.chapters:
            ch_str += "  " + str(c.placement) + ": " + c.name + ": " + str(len(c.scenes)) + " scenes\n"
        ch_str = ch_str.rstrip()
        return "(Book) " + self.name + " (" + str(self.placement) + "):\n" \
            + "Contains (" + str(len(self.chapters)) + ") Chapters:\n" \
            + ch_str + "\n" 