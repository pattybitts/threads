class Chapter:

    def __init__(self, title, num):
        self.title = title
        self.viewpoints = []
        self.number = num

    def add_viewpoint(self, new_vp):
        self.viewpoints.append(new_vp)

    def print_chapter(self):
        out = "(Chapter) " + self.title + " (" + str(self.number) + "):\n"
        for vp in self.viewpoints:
            out += "  VP " + str(vp.number) + ":\n"
            out += str(vp.print_viewpoint()) + "\n"
        return out