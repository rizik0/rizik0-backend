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
            {"name": "alaska", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "northwest_territory", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "alberta", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "ontario", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "greenland", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "quebec", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "western_united_states", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "eastern_united_states", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "central_america", "troups": 0, "owner": None, "continent": "north-america", "neibourghs": []},
            {"name": "venezuela", "troups": 0, "owner": None, "continent": "south-america", "neibourghs": []},
            {"name": "peru", "troups": 0, "owner": None, "continent": "south-america", "neibourghs": []},
            {"name": "brazil", "troups": 0, "owner": None, "continent": "south-america", "neibourghs": []},
            {"name": "argentina", "troups": 0, "owner": None, "continent": "south-america", "neibourghs": []},
            {"name": "iceland", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "scandinavia", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "ukraine", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "great_britain", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "northern_europe", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "western_europe", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "southern_europe", "troups": 0, "owner": None, "continent": "europe", "neibourghs": []},
            {"name": "north_africa", "troups": 0, "owner": None, "continent": "africa", "neibourghs": []},
            {"name": "egypt", "troups": 0, "owner": None, "continent": "africa", "neibourghs": []},
            {"name": "east_africa", "troups": 0, "owner": None, "continent": "africa", "neibourghs": []},
            {"name": "congo", "troups": 0, "owner": None, "continent": "africa", "neibourghs": []},
            {"name": "south_africa", "troups": 0, "owner": None, "continent": "africa", "neibourghs": []},
            {"name": "madagascar", "troups": 0, "owner": None, "continent": "africa", "neibourghs": []},
            {"name": "ural", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "siberia", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "yakutsk", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "kamchatka", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "irkutsk", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "mongolia", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "china", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "afghanistan", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "middle_east", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "india", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "siam", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "japan", "troups": 0, "owner": None, "continent": "asia", "neibourghs": []},
            {"name": "indonesia", "troups": 0, "owner": None, "continent": "oceania", "neibourghs": []},
            {"name": "new_guinea", "troups": 0, "owner": None, "continent": "oceania", "neibourghs": []},
            {"name": "western_australia", "troups": 0, "owner": None, "continent": "oceania", "neibourghs": []},
            {"name": "eastern_australia", "troups": 0, "owner": None, "continent": "oceania", "neibourghs": []}
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
    

    