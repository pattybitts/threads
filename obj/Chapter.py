from Scene import Scene

class Chapter:

    def __init__(self, title, num):
        self.name = title
        self.position = num
        self.scenes = []
        #wordcount = 0
        #firstword = 0

    def print_chapter(self):
        out = "(Chapter) " + self.title + " (" + str(self.number) + "):\n"
        return out