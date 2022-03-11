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
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.ai = ai
        self.path = path

    def __repr__(self):
        return f"Entity({self.x}, {self.y}, {self.z}, " \
               f"{self.char}, {self.color}, {self.name}, " \
               f"{self.blocks_movement}, {self.hp}, {self.attack}, {self.defense}, " \
               f"{self.ai}, {self.path})"
