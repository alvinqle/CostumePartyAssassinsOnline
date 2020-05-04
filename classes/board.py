import copy
import random
import time

from config.constants import ASSASSINS
from config.constants import Color
from .room import Room

random.seed(time.time())


class Board:

    adjaceny_map = {
        'BLUE': ['GRAY', 'RED', 'YELLOW'],
        'GRAY': ['BLUE', 'GREEN', 'RED', 'YELLOW'],
        'GREEN': ['GRAY', 'RED', 'YELLOW'],
        'RED': ['BLUE', 'GRAY', 'GREEN'],
        'YELLOW': ['BLUE', 'GRAY', 'GREEN']
    }

    def __init__(self):
        self.assassin_pool = ASSASSINS
        self.assassin_locations = {}
        random.shuffle(self.assassin_pool)
        self.rooms = {
            Color.BLUE.name: Room(Color.BLUE, self.assassin_pool[0:4]),
            Color.GRAY.name: Room(Color.GRAY, self.assassin_pool[4:8]),
            Color.GREEN.name: Room(Color.GREEN, self.assassin_pool[8:12]),
            Color.RED.name: Room(Color.RED, self.assassin_pool[12:16]),
            Color.YELLOW.name: Room(Color.YELLOW, self.assassin_pool[16:])
        }
        for assassin in self.assassin_pool:
            if assassin in self.rooms['BLUE'].get_occupants():
                self.assassin_locations[assassin] = 'BLUE'
            elif assassin in self.rooms['GRAY'].get_occupants():
                self.assassin_locations[assassin] = 'GRAY'
            elif assassin in self.rooms['GREEN'].get_occupants():
                self.assassin_locations[assassin] = 'GREEN'
            elif assassin in self.rooms['RED'].get_occupants():
                self.assassin_locations[assassin] = 'RED'
            elif assassin in self.rooms['YELLOW'].get_occupants():
                self.assassin_locations[assassin] = 'YELLOW'
        random.shuffle(self.assassin_pool)

    def assassins_remain(self):
        return self.assassin_pool == []

    def display_state(self):
        board_state = self.get_state()
        print(board_state)

    def get_state(self):
        board_state = {
            'assassin_locations': copy.deepcopy(self.assassin_locations),
            'assassin_pool': copy.deepcopy(self.assassin_pool)
        }
        return board_state
