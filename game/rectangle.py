class Rectangle:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def __repr__(self):
        return f"Rectangle({self.x1}, {self.y1}, {self.x2-self.x1}, {self.y2-self.y1})"


def center(rect):
    center_x = int((rect.x1 + rect.x2) / 2)
    center_y = int((rect.y1 + rect.y2) / 2)
    return center_x, center_y


def inner(rect):
    return slice(rect.x1+1, rect.x2), slice(rect.y1+1, rect.y2)


def intersects(rect1, rect2):
    return (
        rect1.x1 <= rect2.x2
        and rect1.x2 >= rect2.x1
        and rect1.y1 <= rect2.y2
        and rect1.y2 >= rect2.y1
    )
