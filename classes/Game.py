from classes.Player import Player
from random import shuffle, randint
import uuid

class Game:

    def __init__(self) -> None:
        self.game_id = str(uuid.uuid4())
        self.possible_goals = ["Conquere North America", "Conquere South America", "Conquere Europe", "Conquere Africa", "Conquere Asia", "Conquere Oceania"]
        self.players = []
        self.status = "Waiting for players to join..."
        self.map = [
            {"name": "alaska", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "northwest_territory", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "alberta", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "ontario", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "greenland", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "quebec", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "western_united_states", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "eastern_united_states", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "central_america", "troops": 0, "owner": None, "continent": "north-america", "neighbours": []},
            {"name": "venezuela", "troops": 0, "owner": None, "continent": "south-america", "neighbours": []},
            {"name": "peru", "troops": 0, "owner": None, "continent": "south-america", "neighbours": []},
            {"name": "brazil", "troops": 0, "owner": None, "continent": "south-america", "neighbours": []},
            {"name": "argentina", "troops": 0, "owner": None, "continent": "south-america", "neighbours": []},
            {"name": "iceland", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "scandinavia", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "ukraine", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "great_britain", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "northern_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "western_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "southern_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": []},
            {"name": "north_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": []},
            {"name": "egypt", "troops": 0, "owner": None, "continent": "africa", "neighbours": []},
            {"name": "east_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": []},
            {"name": "congo", "troops": 0, "owner": None, "continent": "africa", "neighbours": []},
            {"name": "south_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": []},
            {"name": "madagascar", "troops": 0, "owner": None, "continent": "africa", "neighbours": []},
            {"name": "ural", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "siberia", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "yakutsk", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "kamchatka", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "irkutsk", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "mongolia", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "china", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "afghanistan", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "middle_east", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "india", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "siam", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "japan", "troops": 0, "owner": None, "continent": "asia", "neighbours": []},
            {"name": "indonesia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": []},
            {"name": "new_guinea", "troops": 0, "owner": None, "continent": "oceania", "neighbours": []},
            {"name": "western_australia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": []},
            {"name": "eastern_australia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": []}
        ]

        
    def current_game_status(self) -> str:
        return f"Game ID: {self.game_id}\nPlayers: {self.players}" 

    def join_players(self, player1: str, player2: str, player3: str) -> None:
        self.add_player(player1)
        self.add_player(player2)
        self.add_player(player3)
        self.shuffle_players()

    
    def assing_map_randomly(self) -> None:
        pass


    def add_player(self, player: str) -> None:
        self.players.append(Player(player, self.possible_goals.pop(randint(0, len(self.possible_goals)-1))))
        
        
    def shuffle_players(self) -> None:
        shuffle(self.players)
    

    