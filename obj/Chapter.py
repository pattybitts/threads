from obj.Scene import Scene

class Chapter:

    def __init__(self, title, num):
        self.name = title
        self.placement = num
        self.scenes = []

    #all methods below are before 1-19

    def print_chapter(self):
        out = "(Chapter) " + self.title + " (" + str(self.number) + "):\n"
        return out