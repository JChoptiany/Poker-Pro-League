import sqlite3
from datetime import date
from datetime import datetime
from Result import Result
from Player import Player
from Match import Match


class DatabaseConnector:
    def __init__(self, file_name: str = 'poker.db'):
        self.connection = sqlite3.connect(file_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_tables_if_dont_exist()

    def create_tables_if_dont_exist(self):
        self.cursor.executescript("""
                                    CREATE TABLE IF NOT EXISTS Players (
                                        nickname varchar(30) NOT NULL PRIMARY KEY,                                        
                                        first_name varchar(30) NOT NULL,
                                        last_name varchar(30) NOT NULL,
                                        date_of_birth datetime NOT NULL,
                                        gender varchar(1) NOT NULL,
                                        password varchar(50) NOT NULL
                                    )""")

        self.cursor.executescript("""
                                    CREATE TABLE IF NOT EXISTS Results (
                                        id INTEGER PRIMARY KEY ASC,
                                        match_date datetime NOT NULL,
                                        place int NOT NULL,
                                        player_nickname int NOT NULL,
                                        FOREIGN KEY(player_nickname) REFERENCES Players(nickname)                                            
                                  )""")

        self.cursor.executescript("""
                                    CREATE TABLE IF NOT EXISTS Matches (
                                        id INTEGER PRIMARY KEY ASC,
                                        date datetime NOT NULL,
                                        expected_players NOT NULL,
                                        confirmed_players NOT NULL,
                                        entry_fee INTEGER NOT NULL
                                  )""")

    def add_result(self, result: Result) -> None:
        self.cursor.execute(
            'INSERT INTO Results VALUES(NULL, ?, ?, ?);',
            (result.date, result.place, result.player.nickname)
        )
        self.connection.commit()

    def add_results(self, results) -> None:
        for result in results:
            self.add_result(result)

    def add_player(self, player: Player) -> None:
        self.cursor.execute(
            'INSERT INTO Players VALUES(?, ?, ?, ?, ?, ?);',
            (player.nickname, player.first_name, player.last_name, player.date_of_birth, player.gender, player.password)
        )
        self.connection.commit()

    def add_players(self, players) -> None:
        for player in players:
            self.add_player(player)

    def get_player_by_nickname(self, nickname: str) -> Player:
        self.cursor.execute("SELECT first_name, last_name, date_of_birth, gender, nickname, password FROM Players WHERE nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        player = Player(response[0][0], response[0][1], date.fromisoformat(response[0][2]), response[0][3], response[0][4], response[0][5])
        return player

    def remove_player_by_nickname(self, nickname: str) -> None:
        self.cursor.execute("DELETE FROM Players WHERE Players.nickname = ?", (nickname,))

    def get_result_by_id(self, id) -> Result:
        self.cursor.execute("SELECT * FROM Players WHERE id = (?)", id)
        response = self.cursor.fetchall()

        result = Result(datetime.fromisoformat(response[0][0]), response[0][1], response[0][2], self.get_player_by_id(response[3]))
        return result
    
    def remove_all_the_player_results_by_nickname(self, nickname: str) -> None:
        self.cursor.execute("DELETE FROM Results WHERE Results.player_nickname = ?", (nickname,))
    
    def remove_all_the_results(self) -> None:
        self.cursor.execute("DELETE FROM Results")

    def get_all_the_results(self) -> list:
        self.cursor.execute("SELECT match_date, place, player_nickname, Results.id FROM Results INNER JOIN Players on Players.nickname = Results.player_nickname")
        response = self.cursor.fetchall()
        results = []
        for raw_result in response:
            results.append(Result(datetime.fromisoformat(raw_result[0]), raw_result[1], self.get_player_by_nickname(raw_result[2]), raw_result[3]))

        return results
    
    def change_player_nickname(self, current_nickname: str, new_nickname: str) -> None:
        self.cursor.execute("UPDATE Players SET nickname = ? WHERE nickname = ?", (new_nickname, current_nickname))
        self.cursor.execute("UPDATE Results SET player_nickname = ? WHERE player_nickname = ?", (new_nickname, current_nickname))

    def get_all_the_players(self) -> list:
        self.cursor.execute("SELECT first_name, last_name, date_of_birth, gender, nickname, password FROM Players")
        response = self.cursor.fetchall()
        players = []
        for raw_player in response:
            players.append(Player(raw_player[0], raw_player[1], raw_player[2], raw_player[3], raw_player[4], raw_player[5]))

        return players
    
    def get_all_the_player_results_by_nickname(self, nickname: str) -> list:
        self.cursor.execute("SELECT match_date, place, player_nickname, id FROM Results WHERE player_nickname = ?", (nickname,))
        response = self.cursor.fetchall()
        results = []

        for raw_result in response:
            results.append(Result(datetime.fromisoformat(raw_result[0]), int(raw_result[1]), raw_result[2], int(raw_result[3])))

        return results
    
    def get_number_of_matches(self) -> int:
        self.cursor.execute("SELECT COUNT (DISTINCT match_date) AS 'Match' FROM Results")
        response = self.cursor.fetchall()

        number_of_matches = response[0][0]
        return number_of_matches
    
    def get_recent_match_date(self) -> str:
        self.cursor.execute("SELECT MAX(match_date) FROM Results")
        response = self.cursor.fetchall()

        number_of_matches = response[0][0]
        return number_of_matches
    
    def get_number_of_players(self) -> int:
        self.cursor.execute("SELECT COUNT(nickname) FROM Players")
        response = self.cursor.fetchall()

        number_of_players = response[0][0]
        return number_of_players

    def is_player_registered(self, nickname: str) -> bool:
        self.cursor.execute("SELECT COUNT(nickname) FROM Players WHERE nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        number_of_appearances = int(response[0][0])
        return number_of_appearances > 0
    
    def get_number_of_players_in_match_by_date(self, date: datetime) -> int:
        self.cursor.execute("SELECT COUNT(player_nickname) FROM Results WHERE match_date = ?", (date.date(),))
        response = self.cursor.fetchall()

        number_of_players = int(response[0][0])
        return number_of_players

    def get_ranking_table(self):
        player_scores = []
        for player in self.get_all_the_players():
            player_data = {}
            player_data['name'] = player.get_full_name()
            player_data['points'] = 0
            player_data['position'] = '-'
            player_data['wins'] = 0
            player_data['matches'] = 0

            for result in self.get_all_the_player_results_by_nickname(player.nickname):
                player_data['matches'] += 1
                if result.place == 1:
                    player_data['wins'] += 1
                player_data['points'] += self.get_number_of_players_in_match_by_date(result.date) - result.place + 1                

            player_scores.append(player_data)

        player_scores = sorted(player_scores, key=lambda player_data: (-player_data['points'], -player_data['wins'], player_data['name'])) 

        for index, player_data in enumerate(player_scores):
            if player_data['matches'] > 0:
                player_data['position'] = str(index+1)

        return player_scores
        
    def validate_player_date_of_birth(self, nickname: str, given_date_of_birth: date) -> bool:
        self.cursor.execute("SELECT date_of_birth FROM Players WHERE nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        if response:
            actual_date_of_birth = response[0][0]
            return given_date_of_birth == actual_date_of_birth
        else:
            return False

    def get_full_player_statistics(self, player: Player) -> list:
        player_data = {}
        player_data['full_name'] = player.first_name + ' ' + player.last_name
        player_data['gender'] = player.gender
        player_data['matches_played'] = 0
        player_data['frequency'] = 0
        player_data['wins'] = 0
        player_data['win_rate'] = 0
        player_data['podiums'] = 0
        player_data['podium_rate'] = 0
        player_data['recent_win'] = self.get_recent_win_by_nickname(player.nickname)
        player_data['highest_place'] = self.get_highest_place_by_nickname(player.nickname)
        player_data['recent_place'] = self.get_recent_place_by_nickname(player.nickname)
        player_data['recent_match_date'] = self.get_recent_match_date_by_nickname(player.nickname)
        player_data['highest_place'] = self.get_highest_place_by_nickname(player.nickname)
        player_data['average_place'] = self.get_average_place_by_nickname(player.nickname)
        player_data['opponents_beaten'] = self.get_number_of_opponents_beaten_by_nickname(player.nickname)
        player_data['form'] = self.get_form_by_nickname(player.nickname)
        player_data['points'] = 0

        ranking = self.get_ranking_table()
        for record in ranking:
            if record['name'] == player_data['full_name']:
                player_data['position'] = int(record['position'])
                break

        for result in self.get_all_the_player_results_by_nickname(player.nickname):
                player_data['matches_played'] += 1
                if result.place == 1:
                    player_data['wins'] += 1
                if result.place <= 3:
                    player_data['podiums'] += 1
                player_data['points'] += self.get_number_of_players_in_match_by_date(result.date) - result.place + 1    
        
        player_data['attendance'] = int(player_data['matches_played'] / self.get_number_of_matches() * 100)
        player_data['win_rate'] = int(player_data['wins'] / self.get_number_of_matches() * 100)
        player_data['podium_rate'] = int(player_data['podiums'] / self.get_number_of_matches() * 100)


        return player_data

    def get_number_of_matches_played_by_nickname(self, nickname: str) -> int:
        self.cursor.execute("SELECT COUNT(player_nickname) FROM Results WHERE player_nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        if response:
            return int(response[0][0])
        else:
            return '-'

    def get_number_of_wins_by_nickname(self, nickname: str) -> int:
        self.cursor.execute("SELECT COUNT(player_nickname) FROM Results WHERE player_nickname = (?) AND place = 1", (nickname,))
        response = self.cursor.fetchall()

        if response:
            return int(response[0][0])
        else:
            return '-'

    def get_number_of_podiums_by_nickname(self, nickname: str) -> int:
        self.cursor.execute("SELECT COUNT(player_nickname) FROM Results WHERE player_nickname = (?) AND place <= 3", (nickname,))
        response = self.cursor.fetchall()

        if response:
            return int(response[0][0])
        else:
            return '-'
    
    def get_recent_win_by_nickname(self, nickname: str) -> str:
        self.cursor.execute("SELECT MAX(match_date) FROM Results WHERE player_nickname = (?) AND place = 1", (nickname,))
        response = self.cursor.fetchall()

        if response[0][0]:
            return response[0][0]
        else:
            return '-'

    def get_highest_place_by_nickname(self, nickname: str) -> int:
        self.cursor.execute("SELECT MIN(place) FROM Results WHERE player_nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        if response[0][0]:
            return int(response[0][0])
        else:
            return '-'
    
    def get_recent_place_by_nickname(self, nickname: str) -> int:
        self.cursor.execute("SELECT place FROM Results WHERE player_nickname = (?) ORDER BY match_date DESC", (nickname,))
        response = self.cursor.fetchall()

        if response:
            return int(response[0][0])
        else:
            return '-'

    def get_recent_match_date_by_nickname(self, nickname: str) -> str:
        self.cursor.execute("SELECT match_date FROM Results WHERE player_nickname = (?) ORDER BY match_date DESC", (nickname,))
        response = self.cursor.fetchall()

        if response:
            return response[0][0]
        else:
            return '-'
    
    def get_average_place_by_nickname(self, nickname: str) -> float:
        self.cursor.execute("SELECT AVG(place) FROM Results WHERE player_nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        if response[0][0]:
            return float(response[0][0])
        else:
            return '-'
    
    def get_number_of_opponents_beaten_by_nickname(self, nickname: str) -> int:
        self.cursor.execute("SELECT place, match_date FROM Results WHERE player_nickname = (?)", (nickname,))
        response = self.cursor.fetchall()

        number_of_opponents_beaten = 0
        for result in response:
            number_of_opponents_beaten = self.get_number_of_players_in_match_by_date(datetime.fromisoformat(result[1])) - int(result[0])

        return number_of_opponents_beaten
    
    def get_points_by_nickname(self, nickname: str) -> int:
        points = 0
        for result in self.get_all_the_player_results_by_nickname(nickname):
                points += self.get_number_of_players_in_match_by_date(result.date) - result.place + 1              

        return points
    
    def get_all_the_matches(self) -> list:
        self.cursor.execute("SELECT date, entry_fee, expected_players, confirmed_players, id FROM Matches ORDER BY date ASC")
        response = self.cursor.fetchall()
        matches = []
        for raw_match in response:
            matches.append(Match(datetime.fromisoformat(raw_match[0]), int(raw_match[1]), int(raw_match[2]), int(raw_match[3]), int(raw_match[4])))

        return matches
    
    def add_match(self, match: Match) -> None:
        self.cursor.execute(
            'INSERT INTO Matches (date, expected_players, confirmed_players, entry_fee) VALUES(?, ?, ?, ?);',
            (str(match.date), str(match.expected_players), str(match.confirmed_players), str(match.entry_fee))
        )
        self.connection.commit()
    
    def remove_match_by_id(self, id: int) -> None:
        self.cursor.execute("DELETE FROM Matches WHERE id = ?", (id,))
    
    def get_the_next_match(self) -> Match:
        self.cursor.execute("SELECT date, entry_fee, expected_players, confirmed_players, id FROM Matches ORDER BY date ASC LIMIT 1")
        response = self.cursor.fetchall()

        if response:
            return Match(datetime.fromisoformat(response[0][0]), int(response[0][1]), int(response[0][2]), int(response[0][3]), int(response[0][4]))
        else:
            return None
    
    def get_future_matches(self) -> list:
        matches = []
        matches.extend(self.get_all_the_matches())
        if matches:
            del matches[0]
        return matches
    
    def get_number_of_scheduled_matches(self) -> int:
        self.cursor.execute("SELECT COUNT(id) FROM Matches")
        response = self.cursor.fetchall()

        number_of_matches = response[0][0]
        return number_of_matches
    
    def get_match_by_id(self, id: int) -> Match:
        self.cursor.execute("SELECT date, entry_fee, expected_players, confirmed_players, id FROM Matches WHERE id = ?", (id,))
        response = self.cursor.fetchall()

        if response:
            return Match(datetime.fromisoformat(response[0][0]), int(response[0][1]), int(response[0][2], int(response[0][3]), int(response[0][4])))
        else:
            return None   

    def get_maximum_players_in_match(self) -> int:
        self.cursor.execute("SELECT MAX(players) FROM (SELECT COUNT(player_nickname) AS 'players' FROM Results GROUP BY match_date)")
        response = self.cursor.fetchall()

        if response[0][0]:
            return int(response[0][0])
        else:
            return 0

    def get_active_players_percentage(self) -> int:
        self.cursor.execute("SELECT COUNT (DISTINCT player_nickname) AS 'Active players' FROM Results")
        response = self.cursor.fetchall()

        if response[0][0]:
            return int(100 * int(response[0][0]) / self.get_number_of_players())
        else:
            return 0

    def validate_match_date(self, id: int, given_date: datetime) -> bool:
        self.cursor.execute("SELECT date FROM Matches WHERE id = (?)", (id,))
        response = self.cursor.fetchall()
        
        if response:
            actual_date = datetime.fromisoformat(response[0][0])
            return given_date.date() == actual_date.date()
        else:
            return False
        
    def get_age_gap(self) -> int:
        min_age = -1
        max_age = -1
        players = self.get_all_the_players()

        if len(players) > 1:
            for player in players:
                if player.get_age() < min_age or min_age == -1:
                    min_age = player.get_age()
                if player.get_age() > max_age:
                    max_age = player.get_age()
            return max_age - min_age
        else:
            return 0
    
    def get_form_by_nickname(self, nickname: str) -> str:
        results = self.get_all_the_player_results_by_nickname(nickname)
        
        if len(results) > 1:
            change = results[1].place - results[0].place
            if change > 0:
                return f'🔼 {change}'
            elif change < 0:
                return f'🔽 {-change}'
            return '⚫ stable'
        else:
            return '-'
    
    def get_total_points(self) -> int:
        sum = 0
        for player in self.get_ranking_table():
            sum += player['points']
        
        return sum
    
    def get_number_of_results(self) -> int:
        self.cursor.execute("SELECT COUNT(id) FROM Results")
        response = self.cursor.fetchall()
        
        if response:
            return int(response[0][0])
        else:
            return 0

    def get_total_coins_played(self) -> int:
        return 100_000 * self.get_number_of_results()

    def remove_outdated_matches(self) -> None:
        self.cursor.execute("DELETE FROM Matches WHERE date < datetime('now')")
