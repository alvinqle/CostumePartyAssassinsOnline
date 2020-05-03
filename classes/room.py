from enum import Enum


class Color(Enum):
    BLACK = 0
    BLUE = 1
    GRAY = 2
    GREEN = 3
    RED = 4
    YELLOW = 5


class Room:

    def __init__(self, color: Color, assassins: list):
        self.color = color
        self.occupants = assassins

    def get_color(self) -> Color:
        return self.color

    def get_occupants(self) -> set:
        return set(self.occupants)

    def is_empty(self) -> bool:
        return self.occupants == []

    def display(self):
        print(self.occupants)
