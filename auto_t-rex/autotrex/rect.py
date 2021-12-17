class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple:
        return (self.x, self.y)


class Rect:
    def __init__(self, x, y, w, h) -> None:
        self.top_left: Point = Point(x, y)
        self.bottom_right: Point = Point(x + w, y + h)

    @property
    def width(self):
        return self.bottom_right.x - self.top_left.x
    
    @property
    def height(self):
        return self.bottom_right.y - self.top_left.y