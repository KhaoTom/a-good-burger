import numpy
import tcod


tile_dt = numpy.dtype(
    [
        ("walkable", numpy.bool),  # true if tile can be walked over
        ("transparent", numpy.bool),  # true if tile doesnt block fov
        ("dark", tcod.console.rgb_graphic),  # graphic for when tile is not in fov
        ("light", tcod.console.rgb_graphic),  # graphic for when tile is in fov
    ]
)


def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
        light: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> numpy.ndarray:
    return numpy.array((walkable, transparent, dark, light), dtype=tile_dt)


unexplored = numpy.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=tcod.console.rgb_graphic)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), (15, 15, 75), (0, 0, 0)),
    light=(ord("."), (65, 65, 45), (0, 0, 0)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (0, 0, 0), (45, 45, 45)),
    light=(ord(" "), (0, 0, 0), (95, 95, 95)),
)
