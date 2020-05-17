class Book:

    def __init__(self, title, num):
        self.title = title
        self.number = num
        self.chapters = []

    def add_chapter(self, new_chapter):
        self.chapters.append(new_chapter)