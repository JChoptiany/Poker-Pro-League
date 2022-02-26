import datetime
from Generators import generate_password, generate_nickname


class Player:
    def __init__(self, first_name: str, last_name: str, date_of_birth: str, gender: str, nickname: str = None, password: str = None):
        self.first_name = first_name
        self.last_name = last_name
        if isinstance(date_of_birth, datetime.date):
            self.date_of_birth = date_of_birth.strftime('%Y-%m-%d')
        else:
            self.date_of_birth = date_of_birth
        self.gender = gender
        self.nickname = nickname = nickname if nickname != None else generate_nickname(self.first_name, self.last_name, self.date_of_birth)
        self.password = password = password if password != None else generate_password()
    
    def get_age(self) -> int:
        return int((datetime.date.today().year - datetime.date.fromisoformat(self.date_of_birth).year))
    
    def get_full_name(self) -> str:
        return self.first_name + ' ' + self.last_name
