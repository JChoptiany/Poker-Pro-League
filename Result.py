from datetime import datetime
import Player


class Result:
    def __init__(self, date: datetime, place: int, player: Player, id: int = None):
        self.id = id
        self.date = date
        self.place = place
        self.player = player
