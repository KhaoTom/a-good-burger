import copy


class Entity:
    def __init__(self, x, y, char, color, name, blocks_movement):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def melee(self, target):
        print(f"{self.name} kicked {target.name}!")

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def clone(self, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        return clone
