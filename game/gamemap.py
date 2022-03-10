import numpy


class GameMap:
    def __init__(self, width, height, entities, fill_tile):
        self.width = width
        self.height = height
        self.tiles = numpy.full((width, height), fill_value=fill_tile, order="F")
        self.visible = numpy.full((width, height), fill_value=False, order="F")
        self.explored = numpy.full((width, height), fill_value=False, order="F")
        self.entities = set(entities)
