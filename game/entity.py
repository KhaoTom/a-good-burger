import copy


class Entity:
    def __init__(self, x, y, z, char, color, name, blocks_movement, stats, ai, path):
        self.x = x
        self.y = y
        self.z = z
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.stats = stats
        self.ai = ai
        self.path = path

    def clone(self, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        return clone