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
