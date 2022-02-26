import datetime

class Match:
    def __init__(self, date: datetime.datetime, entry_fee: int, expected_players: int, confirmed_players: int ,id: int = 0):
        self.date = date
        self.entry_fee = entry_fee
        self.expected_players = expected_players
        self.confirmed_players = confirmed_players
        self.id = id
    
    def add_cofirmation(self, number_of_new_confirmations: int = 1) -> None:
        self.confirmed_players += number_of_new_confirmations
    
    def get_date(self) -> str:
        return self.date.strftime('%d.%m.%Y')
    
    def get_time(self) -> str:
        return self.date.strftime('%H:%M')

    def get_time_left(self) -> str:
        timedelta = self.date - datetime.datetime.now()
        seconds = timedelta.total_seconds()
        days = round(seconds / 86400)
        hours = round(seconds / 3600)

        if days > 300:
            return "A lot of time left..."
        if days > 35:
            months = int(days / 30)
            days -= months * 30
            return f"{months} months, {days} days"
        if days > 1:
            return f"{days} days"
        if days == 1:
            return "1 day"
        if hours > 1:
            return f"{hours} hours"
        if hours == 1:
            return "1 hour"
        return "Starting soon..."
    