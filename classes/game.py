from pprint import pprint
import random
import uuid

from classes.board import Board
from classes.player import Player
from config.constants import Color


class Game:

    def __init__(self, player_usernames: list):
        lives = 1 if len(player_usernames) > 8 else 2  # If there are more than 8 players, each player has 1 assassin
        self.board = Board()
        self.players = {}
        self.current_turn = {
            'players': {}
        }
        self.state = {
            'turns': []
        }

        for index, username in enumerate(player_usernames):
            player_id = str(uuid.uuid4())
            self.players[player_id] = Player(username=username)
            self.players[player_id].player_id = player_id
            for i in range(lives):
                assassin = self.board.assassin_pool.pop()
                self.players[player_id].assassins[assassin] = self.board.assassin_locations[assassin]
                self._log_player_state_on_turn(self.players[player_id])
            # self.players[player_id].display()

        self._log_board_state_on_turn()
        self.turn_order = list(self.players.keys())
        random.shuffle(self.turn_order)
        # self.board.display()

    @staticmethod
    def roll_dice() -> int:
        return random.randint(0, 5)

    def _log_board_state_on_turn(self):
        board_state = self.board.get_state()
        self.current_turn['board'] = board_state

    def _log_player_state_on_turn(self, player):
        player_state = player.get_state()
        self.current_turn['players'][player.player_id] = player_state

    def _save_turn_state(self, turn):
        self.state['turns'].append(turn)

    def action(self, player: Player, room_color: str):

        def _option_is_valid(option, max_option: int) -> bool:
            if not isinstance(option, int):
                return False
            if option < 1 or option > max_option:
                return False
            return True

        def _black_action():

            def _build_kill_string() -> str:
                kill_string = ''
                count = 1
                for kill_option in actionable_assassins:  # Building the list of options to print out
                    kill_string += f'{count}. Assassinate the {kill_option} in ' \
                                   f'{self.board.assassin_locations[kill_option]} room.\n'
                    count += 1
                return kill_string

            def _draw_from_deck(username, draw_count):
                assassin_drawn = self.board.assassin_pool.pop()
                print(f'{assassin_drawn} was drawn from the deck and killed! {username} has '
                      f'{2 - draw_count} draws left.')

            # Get list of assassins that the player can affect
            actionable_assassins = []
            for color in self.board.adjaceny_map.keys():
                if self.occupies_room(player=player, room_color=color):
                    actionable_assassins.extend(self.board.rooms[color].occupants)
            for assassin in player.assassins.keys():
                if assassin in actionable_assassins:
                    actionable_assassins.remove(assassin)

            option_string = 'Please choose an action to execute.\n\n'

            if self.board.assassins_remain() and player.draw_count < 2:  # If an assassin from the pool can be drawn
                if actionable_assassins:  # If there are assassins that the player can affect
                    option_string += _build_kill_string()
                    option_count = len(actionable_assassins) + 1  # Continuing the option count from the last assassin
                    option_string += f'{option_count}. Draw an assassin from the deck.'

                    while True:
                        option = int(input(option_string))
                        if _option_is_valid(option=option, max_option=len(actionable_assassins) + 1):
                            break
                        else:
                            print('Please enter a valid option from the list.\n')

                    if option <= len(actionable_assassins):  # Player chooses to kill an assassin
                        chosen_assassin = actionable_assassins[option - 1]
                        self.board.rooms[self.board.assassin_locations[chosen_assassin]].occupants.remove(
                            chosen_assassin)
                        del self.board.assassin_locations[chosen_assassin]
                        self.board.assassin_pool.remove(chosen_assassin)
                    else:  # A random assassin is drawn from the pool and killed
                        player.draw_count += 1
                        _draw_from_deck(username=player.username, draw_count=player.draw_count)
                else:
                    player.draw_count += 1
                    _draw_from_deck(username=player.username, draw_count=player.draw_count)
            else:  # Either there are no extra assassins left or the player is out of draws
                if actionable_assassins:
                    option_string += _build_kill_string()

                    while True:
                        option = int(input(option_string))
                        if _option_is_valid(option=option, max_option=len(actionable_assassins)):
                            break
                        else:
                            print('Please enter a valid option from the list.\n')

                    chosen_assassin = actionable_assassins[option - 1]
                    # Removing the chosen assassin from the room they are currently in
                    self.board.rooms[self.board.assassin_locations[chosen_assassin]].occupants.remove(chosen_assassin)
                    del self.board.assassin_locations[chosen_assassin]  # "Killing" the assassin permanently
                else:  # The player can't move any assassins and is out of draws
                    option_count = 1
                    option_map = {}
                    for assassin, room in player.assassins.items():
                        option_string += f'{option_count}. Kill your {assassin} in the {room} room.\n'
                        option_map[option_count] = assassin
                        option_count += 1

                    while True:
                        option = int(input(option_string))
                        if _option_is_valid(option=option, max_option=len(player.assassins)):
                            break
                        else:
                            print('Please enter a valid option from the list.\n')

                    # Remove the chosen assassin from the room they are currently in
                    self.board.rooms[self.board.assassin_locations[option_map[option]]].occupants.remove(
                        option_map[option])
                    del self.board.assassin_locations[option_map[option]]  # "Killing" the assassin permanently
                    del player.assassins[option_map[option]]  # Removing assassin from player's playable assassins
                    if len(player.assassins) == 0:  # If player is out of assassins, remove them from turn order
                        del self.turn_order[player.player_id]

        def _non_black_action():
            in_assassins = self.board.rooms[room_color].occupants
            in_length = len(in_assassins)
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

            option = int(input(option_string))
            option_count = 1
            if option <= len(in_assassins):
                assassin_chosen = in_assassins[option - 1]
                option_string = f'Choose a color room to move the {assassin_chosen} to.\n\n'
                for color in self.board.adjaceny_map[room_color]:
                    option_string += f'{option_count}. {color}\n'
                    option_count += 1
                second_option = int(input(option_string))
                room_chosen = self.board.adjaceny_map[room_color][second_option - 1]
                self.board.rooms[room_color].occupants.remove(assassin_chosen)
                self.board.rooms[room_chosen].occupants.append(assassin_chosen)
                self.board.assassin_locations[assassin_chosen] = room_chosen
                return
            else:
                assassin_chosen = out_assassins[option - in_length - 1]
                self.board.rooms[self.board.assassin_locations[assassin_chosen]].occupants.remove(assassin_chosen)
                self.board.rooms[room_color].occupants.append(assassin_chosen)
                self.board.assassin_locations[assassin_chosen] = room_color
                return

        if room_color == 'BLACK':
            _black_action()
        else:
            _non_black_action()

    def occupies_room(self, player, room_color) -> bool:
        if room_color != 'BLACK':
            for assassin in self.players[player.player_id].assassins:
                if assassin in self.board.rooms[room_color].get_occupants():
                    return True
            return False
        return False

    def start_game(self) -> None:
        turn_count, self.current_turn['turn'] = 0, 0
        self._save_turn_state(self.current_turn)
        pprint(self.state)
        self.current_turn = {
            'players': {}
        }

        while len(self.turn_order) > 1:
            turn_count += 1
            print(f'Turn {turn_count}\n-------')
            for index, player in enumerate(self.turn_order):
                roll = self.roll_dice()
                print(f'{self.players[player].username} rolled {Color(roll).name}.')
                self.action(player=self.players[player], room_color=Color(roll).name)
                self._log_player_state_on_turn(player=self.players[player])
            self._log_board_state_on_turn()
            self._save_turn_state(turn=self.current_turn)
            pprint(self.state)
            self.current_turn = {
                'players': {}
            }

        print(f'{self.turn_order[0]} wins!')
