from enum import Enum
from pprint import pprint
import random
import time

random.seed(time.time())
ASSASSINS = [
    'Archaeologist',
    'Astronaut',
    'Clown',
    'Cowboy',
    'Doctor',
    'Frankenstein''s Monster',
    'Gangster',
    'Ghost',
    'Hula Dancer',
    'Mummy',
    'Pirate',
    'Police Officer',
    'Princess',
    'Rock Star',
    'Safari Guide',
    'Sherlock',
    'Superhero',
    'Vampire',
    'Wizard',
    'Zombie'
]


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
        pprint(self.occupants)


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
        self.assassin_loc = {}
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
                self.assassin_loc[assassin] = 'BLUE'
            elif assassin in self.rooms['GRAY'].get_occupants():
                self.assassin_loc[assassin] = 'GRAY'
            elif assassin in self.rooms['GREEN'].get_occupants():
                self.assassin_loc[assassin] = 'GREEN'
            elif assassin in self.rooms['RED'].get_occupants():
                self.assassin_loc[assassin] = 'RED'
            elif assassin in self.rooms['YELLOW'].get_occupants():
                self.assassin_loc[assassin] = 'YELLOW'
        random.shuffle(self.assassin_pool)

    def display(self):
        for color, room in self.rooms.items():
            print(color)
            room.display()


class Player:

    def __init__(self, username: str):
        self.assassins = {}
        self.username = username
        self.draw_count = 0
        self.player_id = None

    def is_alive(self) -> bool:
        return self.assassins == []

    def display(self):
        print(self.assassins)


class Game:

    def __init__(self, player_usernames: list):
        self.board = Board()
        self.state = {}
        self.players = {}
        for index, username in enumerate(player_usernames):
            self.players[f'player{index}'] = Player(username=username)
            self.players[f'player{index}'].player_id = f'player{index}'
            for i in range(2):
                self.players[f'player{index}'].assassins[self.board.assassin_pool[index]] \
                    = self.board.assassin_loc[self.board.assassin_pool[index]]
            if index == len(player_usernames) - 1:
                self.remaining_assassins = self.board.assassin_pool[index + 1:]
            self.players[f'player{index}'].display()
        self.turn_order = list(self.players.keys())
        random.shuffle(self.turn_order)
        self.current_turn = self.turn_order[0]  # Set first turn to 0th index of turn order
        self.board.display()

    @staticmethod
    def roll_dice() -> int:
        return random.randint(0, 5)

    def action(self, player: Player, room_color: str):
        if room_color == 'BLACK':
            option_string = 'Please choose an action to execute.\n\n'
            actionable_assassins = []
            for color in self.board.adjaceny_map.keys():
                if self.occupies_room(player=player, room_color=color):
                    actionable_assassins.extend(self.board.rooms[color].occupants)
            for assassin in player.assassins.keys():
                if assassin in actionable_assassins:
                    actionable_assassins.remove(assassin)
            if self.assassins_remain() and player.draw_count < 2:
                if actionable_assassins:
                    option_count = 1
                    for assassin in actionable_assassins:
                        option_string += f'{option_count}. Assassinate the {assassin} in ' \
                                         f'{self.board.assassin_loc[assassin]} room.\n'
                        option_count += 1
                    option_string += f'{option_count}. Draw an assassin from the deck.'
                    option = int(input())  # TODO: Implement correct option checking
                    if option <= len(actionable_assassins):
                        chosen_assassin = actionable_assassins[option - 1]
                        self.board.rooms[self.board.assassin_loc[chosen_assassin]].occupants.remove(chosen_assassin)
                        del self.board.assassin_loc[chosen_assassin]
                        return
                    else:
                        self.remaining_assassins.pop()
                        player.draw_count += 1
                        return
                else:
                    self.remaining_assassins.pop()
                    player.draw_count += 1
                    return
            else:
                if actionable_assassins:
                    option_count = 1
                    for assassin in actionable_assassins:
                        option_string += f'{option_count}. Assassinate the {assassin} in the' \
                                         f'{self.board.assassin_loc[assassin]} room.\n'
                        option_count += 1
                    option = int(input())
                    chosen_assassin = actionable_assassins[option - 1]
                    self.board.rooms[self.board.assassin_loc[chosen_assassin]].occupants.remove(chosen_assassin)
                    del self.board.assassin_loc[chosen_assassin]
                    return
                else:
                    option_count = 1
                    option_map = {}
                    for assassin, room in player.assassins.items():
                        option_string += f'{option_count}. Kill your {assassin} in the {room} room.\n'
                        option_map[option_count] = assassin
                        option_count += 1
                    option = int(input())
                    self.board.rooms[self.board.assassin_loc[option_map[option]]].occupants.remove(option_map[option])
                    del self.board.assassin_loc[option_map[option]]
                    del player.assassins[option_map[option]]
                    if len(player.assassins) == 0:
                        del self.turn_order[player.player_id]
        else:
            in_assassins = self.board.rooms[room_color].occupants
            out_assassins = []
            for adjacent_room in self.board.adjaceny_map[room_color]:
                out_assassins.extend(self.board.rooms[adjacent_room].occupants)
            option_count = 1
            option_string = 'Choose an action:\n\n'

            for assassin in in_assassins:
                option_string += f'{option_count}. Move {assassin} out of {room_color} room.\n'
                option_count += 1
            option_string += '\n'
            for assassin in out_assassins:
                option_string += f'{option_count}. Move {assassin} into {room_color} room.\n'
                option_count += 1
            option_string += '\n'

            print(option_string)
            option = int(input())
            option_count = 1
            if option <= len(in_assassins):
                assassin_chosen = in_assassins[option - 1]
                option_string = f'Choose a color room to move the {assassin_chosen} to.\n\n'
                for color in self.board.adjaceny_map[room_color]:
                    option_string += f'{option_count}. {color}\n'
                    option_count += 1
                print(option_string)
                second_option = int(input())
                room_chosen = self.board.adjaceny_map[room_color][second_option - 1]
                self.board.rooms[room_color].occupants.remove(assassin_chosen)
                self.board.rooms[room_chosen].occupants.append(assassin_chosen)
                self.board.assassin_loc[assassin_chosen] = room_chosen
                return
            else:
                assassin_chosen = out_assassins[option - 1]
                self.board.rooms[self.board.assassin_loc[assassin_chosen]].occupants.remove(assassin_chosen)
                self.board.rooms[room_color].occupants.append(assassin_chosen)
                self.board.assassin_loc[assassin_chosen] = room_color
                return

    def assassins_remain(self) -> bool:
        return self.remaining_assassins == []

    def occupies_room(self, player, room_color) -> bool:
        if room_color != 'BLACK':
            for assassin in self.players[player].assassins:
                if assassin in self.board.rooms[room_color].get_occupants():
                    return True
            return False
        return False

    def start_game(self) -> None:
        turn_count = 1
        while len(self.turn_order) > 1:
            print(turn_count)
            for index, player in enumerate(self.turn_order):
                input(f'{player}: Press Enter to roll the dice...')
                roll = self.roll_dice()
                print(f'Rolled {Color(roll).name}')
                self.action(player=self.players[player], room_color=Color(roll).name)
            turn_count += 1


game = Game(['user1', 'user2'])
game.start_game()
