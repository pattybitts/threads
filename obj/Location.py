class Location:

    def __init__(self, name: str, x_co: int=0, y_co: int=0):
        self.name = name
        self.coordinates = {"x": x_co, "y": y_co}