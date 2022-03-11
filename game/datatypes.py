class Dungeon:
    def __init__(self, width, height, entities, tiles, visible, explored):
        self.width = width
        self.height = height
        self.entities = entities
        self.tiles = tiles
        self.visible = visible
        self.explored = explored

    def __repr__(self):
        return f"GameMap({self.width}, {self.height}, {self.entities}, {self.tiles}, {self.visible}, {self.explored})"


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def __repr__(self):
        return f"Rectangle({self.x1}, {self.y1}, {self.x2-self.x1}, {self.y2-self.y1})"


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
