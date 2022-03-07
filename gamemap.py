import numpy
import tiletype


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = numpy.full((width, height), fill_value=tiletype.wall, order="F")

        self.tiles[30:33, 22] = tiletype.wall

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
