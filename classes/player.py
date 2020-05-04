import copy


class Player:

    def __init__(self, username: str):
        self.assassins = {}
        self.draw_count = 0
        self.player_id = None
        self.username = username

    def display_state(self):
        player_state = self.get_state()
        print(player_state)

    def get_state(self):
        player_state = {
            'assassins': copy.deepcopy(self.assassins),
            'draw_count': copy.copy(self.draw_count),
            'status': copy.copy(self.is_alive()),
            'username': self.username
        }
        return player_state

    def is_alive(self) -> bool:
        return self.assassins != []
