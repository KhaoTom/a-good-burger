import copy


class Entity:
    def __init__(self, x, y, z, char, color, name, blocks_movement, hp, attack, defense, ai, path):
        self.x = x
        self.y = y
        self.z = z
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.hp = BoundedStat(0, hp, hp)
        self.attack = BoundedStat(0, attack, attack)
        self.defense = BoundedStat(0, defense, defense)
        self.ai = ai
        self.path = path

    def __repr__(self):
        return f"Entity({self.x}, {self.y}, {self.z}, " \
               f"{self.char}, {self.color}, {self.name}, " \
               f"{self.blocks_movement}, {self.hp}, {self.attack}, {self.defense}, " \
               f"{self.ai}, {self.path})"

    def clone(self, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        return clone


class BoundedStat:
    """ Stat value with minimum and maximum bounds. """
    def __init__(self, minimum_value, maximum_value, start_value):
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.current_value = start_value

    def __repr__(self):
        return f"BoundedStat({self.minimum_value}, {self.maximum_value}, {self.current_value})"

    def modify(self, amount):
        self.current_value = max(self.minimum_value, min(self.current_value + amount, self.maximum_value))

    def is_at_minimum(self):
        return self.current_value == self.minimum_value

    def is_at_maximum(self):
        return self.current_value == self.maximum_value
