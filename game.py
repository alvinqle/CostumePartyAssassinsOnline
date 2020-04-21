from enum import Enum
import random
import time

from . import ASSASSINS

random.seed(time.time())


class Color(Enum):
    BLACK = 0
    BLUE = 1
    GREEN = 2
    RED = 3
    YELLOW = 4


class Room:

    def __init__(self, color: Color):
        self.color = color
        self.occupants = []

    def get_color(self):
        return self.color

    def get_occupants(self):
        return self.occupants

    def is_empty(self):
        return self.occupants == []


class Board:

    def __init__(self):
        self.black_room = Room(Color.BLACK)
        self.blue_room = Room(Color.BLUE)
        self.green_room = Room(Color.GREEN)
        self.red_room = Room(Color.RED)
        self.yellow_room = Room(Color.YELLOW)
        self.assassin_pool = ASSASSINS
        random.shuffle(self.assassin_pool)


class Player:

    def __init__(self, username: str):
        self.username = username
        self.assassins = []
        self.state = {}

    def is_alive(self):
        return self.assassins == []

    def get_state(self):
        return self.state


class Game:

    def __init__(self, player_usernames: list):
        self.board = Board()
        self.state = {}
        self.players = {}
        for index, username in enumerate(player_usernames):
            self.players[f'player{index}'] = Player(username=username)
            self.players[f'player{index}'].assassins.append(self.board.assassin_pool[index])
        self.players_alive = len(player_usernames)
        self.next_assassin = len(player_usernames)

    def start_game(self):
        while self.players_alive > 1:

