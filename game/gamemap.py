import numpy


class GameMap:
    def __init__(self, width, height, entities, fill_tile):
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.fill_tile = fill_tile
        self.tiles = numpy.full((width, height), fill_value=self.fill_tile, order="F")
        self.visible = numpy.full((width, height), fill_value=False, order="F")
        self.explored = numpy.full((width, height), fill_value=False, order="F")

    def __repr__(self):
        return f"GameMap({self.width}, {self.height}, {self.entities}, {self.fill_tile})"
