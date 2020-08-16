class ULocation:

    def __init__(self, name: str, x_co: int, y_co: int):
        self.name = name
        self.coordinates = {x: x_co, y: y_co}