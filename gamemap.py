import numpy
import tiletype
from tcod.map import compute_fov


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = numpy.full((width, height), fill_value=tiletype.wall, order="F")
        self.visible = numpy.full((width, height), fill_value=False, order="F")
        self.explored = numpy.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        console.tiles_rgb[0:self.width, 0:self.height] = numpy.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tiletype.UNEXPLORED
        )

    def update_fov(self, x, y):
        self.visible[:] = compute_fov(
            self.tiles["transparent"],
            (x, y),
            radius=8
        )
        self.explored |= self.visible
