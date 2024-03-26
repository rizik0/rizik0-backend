from classes.Player import Player
from random import shuffle, randint
import uuid

class Game:

    def __init__(self) -> None:
        self.game_id = str(uuid.uuid4())
        self.possible_goals = ["Conquer North America", "Conquer South America", "Conquer Europe", "Conquer Africa", "Conquer Asia", "Conquer Oceania"]
        self.players = []
        self.status = "Waiting for players to join..."
        self.map = [
            {"name": "alaska", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["northwest_territory", "alberta", "kamchatka"]},
            {"name": "northwest_territory", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["alaska", "alberta", "ontario", "greenland"]},
            {"name": "alberta", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["alaska", "northwest_territory", "ontario", "western_united_states"]},
            {"name": "ontario", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["northwest_territory", "alberta", "greenland", "quebec", "western_united_states", "eastern_united_states"]},
            {"name": "greenland", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["northwest_territory", "ontario", "quebec", "iceland"]},
            {"name": "quebec", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["ontario", "greenland", "eastern_united_states"]},
            {"name": "western_united_states", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["alberta", "ontario", "eastern_united_states", "central_america"]},
            {"name": "eastern_united_states", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["ontario", "quebec", "western_united_states", "central_america"]},
            {"name": "central_america", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["western_united_states", "eastern_united_states", "venezuela"]},
            {"name": "venezuela", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["central_america", "peru", "brazil"]},
            {"name": "peru", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["venezuela", "brazil", "argentina"]},
            {"name": "brazil", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["venezuela", "peru", "argentina", "north_africa"]},
            {"name": "argentina", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["peru", "brazil"]},
            {"name": "iceland", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["greenland", "scandinavia", "great_britain"]},
            {"name": "scandinavia", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["iceland", "ukraine", "northern_europe"]},
            {"name": "ukraine", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["scandinavia", "northern_europe", "southern_europe", "ural", "afghanistan", "middle_east"]},
            {"name": "great_britain", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["iceland", "western_europe", "northern_europe"]},
            {"name": "northern_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["scandinavia", "ukraine", "southern_europe", "western_europe", "great_britain"]},
            {"name": "western_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["great_britain", "northern_europe", "southern_europe", "north_africa"]},
            {"name": "southern_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["ukraine", "northern_europe", "western_europe", "egypt", "north_africa", "middle_east"]},
            {"name": "north_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["brazil", "western_europe", "southern_europe", "egypt", "east_africa", "congo"]},
            {"name": "egypt", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["southern_europe", "north_africa", "east_africa", "middle_east"]},
            {"name": "east_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["north_africa", "egypt", "congo", "south_africa", "madagascar", "middle_east"]},
            {"name": "congo", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["north_africa", "east_africa", "south_africa"]},
            {"name": "south_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["east_africa", "congo", "madagascar"]},
            {"name": "madagascar", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["east_africa", "south_africa"]},
            {"name": "ural", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ukraine", "siberia", "china", "afghanistan"]},
            {"name": "siberia", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ural", "yakutsk", "irkutsk", "mongolia", "china"]},
            {"name": "yakutsk", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["siberia", "kamchatka", "irkutsk"]},
            {"name": "kamchatka", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["alaska", "yakutsk", "irkutsk", "mongolia", "japan"]},
            {"name": "irkutsk", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["siberia", "yakutsk", "kamchatka", "mongolia"]},
            {"name": "mongolia", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["siberia", "irkutsk", "kamchatka", "japan", "china"]},
            {"name": "china", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ural", "siberia", "mongolia", "afghanistan", "india", "siam"]},
            {"name": "afghanistan", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ukraine", "ural", "china", "middle_east", "india"]},
            {"name": "middle_east", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ukraine", "southern_europe", "egypt", "east_africa", "india", "afghanistan"]},
            {"name": "india", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["china", "afghanistan", "middle_east", "siam"]},
            {"name": "siam", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["china", "indonesia", "india"]},
            {"name": "japan", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["kamchatka", "mongolia"]},
            {"name": "indonesia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["siam", "new_guinea", "western_australia"]},
            {"name": "new_guinea", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["indonesia", "western_australia", "eastern_australia"]},
            {"name": "western_australia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["indonesia", "new_guinea", "eastern_australia"]},
            {"name": "eastern_australia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["new_guinea", "western_australia"]}
        ]

        
    def current_game_status(self) -> str:
        return f"Game ID: {self.game_id}\nPlayers: {self.players}" 

    def join_players(self, player1: str, player2: str, player3: str) -> None:
        self.add_player(player1)
        self.add_player(player2)
        self.add_player(player3)
        self.shuffle_players()

    
    def assigning_map_randomly(self) -> None:
        for player in self.players:
            territories_assigned = 0
            max_territories = 14 #trasformare in costante

            while territories_assigned < max_territories:
                random_num = randint(0, len(self.map)-1)
                if self.map[random_num]["owner"] == None:
                    self.map[random_num]["owner"] = player
                    self.map[random_num]["troops"] = 1 
                    territories_assigned += 1
        pass


    def add_player(self, player: str) -> None:
        self.players.append(Player(player, self.possible_goals.pop(randint(0, len(self.possible_goals)-1))))
        
        
    def shuffle_players(self) -> None:
        shuffle(self.players)
    

    #DEBUG FUNCTIONS
    def print_map(self) -> None:
        for territory in self.map:
            print(territory["name"])
            print(territory["owner"])
            print("\n") 


