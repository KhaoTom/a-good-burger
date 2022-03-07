import numpy

graphic_dt = numpy.dtype(
    [
        ("ch", numpy.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = numpy.dtype(
    [
        ("walkable", numpy.bool),  # true if tile can be walked over
        ("transparent", numpy.bool),  # true if tile doesnt block fov
        ("dark", graphic_dt),  # graphic for when tile is not in fov
    ]
)


def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> numpy.ndarray:
    return numpy.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord("."), (15, 15, 75), (0, 0, 0))
)

wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (0, 0, 0), (0, 0, 95))
)