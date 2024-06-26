from classes.Player import Player
from random import shuffle, randint
import uuid

class Game:

    def __init__(self) -> None:
        self.game_id = str(uuid.uuid4()).split('-')[0]
        self.possible_goals = ["north-america", "south-america", "europe", "africa", "asia", "oceania"]
        self.players = []
        self.status = "waiting"
        self.turn_status = "initial"
        self.maps = [
            {"name": "alaska", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["northwest_territory", "alberta", "kamchatka"], "color": None},
            {"name": "northwest_territory", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["alaska", "alberta", "ontario", "greenland"], "color": None},
            {"name": "alberta", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["alaska", "northwest_territory", "ontario", "western_united_states"], "color": None},
            {"name": "ontario", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["northwest_territory", "alberta", "greenland", "quebec", "western_united_states", "eastern_united_states"], "color": None},
            {"name": "greenland", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["northwest_territory", "ontario", "quebec", "iceland"], "color": None},
            {"name": "quebec", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["ontario", "greenland", "eastern_united_states"], "color": None},
            {"name": "western_united_states", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["alberta", "ontario", "eastern_united_states", "central_america"], "color": None},
            {"name": "eastern_united_states", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["ontario", "quebec", "western_united_states", "central_america"], "color": None},
            {"name": "central_america", "troops": 0, "owner": None, "continent": "north-america", "neighbours": ["western_united_states", "eastern_united_states", "venezuela"], "color": None},
            {"name": "venezuela", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["central_america", "peru", "brazil"], "color": None},
            {"name": "peru", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["venezuela", "brazil", "argentina"], "color": None},
            {"name": "brazil", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["venezuela", "peru", "argentina", "north_africa"], "color": None},
            {"name": "argentina", "troops": 0, "owner": None, "continent": "south-america", "neighbours": ["peru", "brazil"], "color": None},
            {"name": "iceland", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["greenland", "scandinavia", "great_britain"], "color": None},
            {"name": "scandinavia", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["iceland", "ukraine", "northern_europe"], "color": None},
            {"name": "ukraine", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["scandinavia", "northern_europe", "southern_europe", "ural", "afghanistan", "middle_east"], "color": None},
            {"name": "great_britain", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["iceland", "western_europe", "northern_europe"], "color": None},
            {"name": "northern_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["scandinavia", "ukraine", "southern_europe", "western_europe", "great_britain"], "color": None},
            {"name": "western_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["great_britain", "northern_europe", "southern_europe", "north_africa"], "color": None},
            {"name": "southern_europe", "troops": 0, "owner": None, "continent": "europe", "neighbours": ["ukraine", "northern_europe", "western_europe", "egypt", "north_africa", "middle_east"], "color": None},
            {"name": "north_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["brazil", "western_europe", "southern_europe", "egypt", "east_africa", "congo"], "color": None},
            {"name": "egypt", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["southern_europe", "north_africa", "east_africa", "middle_east"], "color": None},
            {"name": "east_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["north_africa", "egypt", "congo", "south_africa", "madagascar", "middle_east"], "color": None},
            {"name": "congo", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["north_africa", "east_africa", "south_africa"], "color": None},
            {"name": "south_africa", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["east_africa", "congo", "madagascar"], "color": None},
            {"name": "madagascar", "troops": 0, "owner": None, "continent": "africa", "neighbours": ["east_africa", "south_africa"], "color": None},
            {"name": "ural", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ukraine", "siberia", "china", "afghanistan"], "color": None},
            {"name": "siberia", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ural", "yakutsk", "irkutsk", "mongolia", "china"], "color": None},
            {"name": "yakutsk", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["siberia", "kamchatka", "irkutsk"], "color": None},
            {"name": "kamchatka", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["alaska", "yakutsk", "irkutsk", "mongolia", "japan"], "color": None},
            {"name": "irkutsk", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["siberia", "yakutsk", "kamchatka", "mongolia"], "color": None},
            {"name": "mongolia", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["siberia", "irkutsk", "kamchatka", "japan", "china"], "color": None},
            {"name": "china", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ural", "siberia", "mongolia", "afghanistan", "india", "siam"], "color": None},
            {"name": "afghanistan", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ukraine", "ural", "china", "middle_east", "india"], "color": None},
            {"name": "middle_east", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["ukraine", "southern_europe", "egypt", "east_africa", "india", "afghanistan"], "color": None},
            {"name": "india", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["china", "afghanistan", "middle_east", "siam"], "color": None},
            {"name": "siam", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["china", "indonesia", "india"], "color": None},
            {"name": "japan", "troops": 0, "owner": None, "continent": "asia", "neighbours": ["kamchatka", "mongolia"], "color": None},
            {"name": "indonesia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["siam", "new_guinea", "western_australia"], "color": None},
            {"name": "new_guinea", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["indonesia", "western_australia", "eastern_australia"], "color": None},
            {"name": "western_australia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["indonesia", "new_guinea", "eastern_australia"], "color": None},
            {"name": "eastern_australia", "troops": 0, "owner": None, "continent": "oceania", "neighbours": ["new_guinea", "western_australia"], "color": None}
        ]
        self.turn = 0
    
    def __str__(self) -> None:
        ret = "Players:\n"
        for player in self.players:
            ret += str(player) + "\n"
        ret += "maps:\n"
        for territory in self.maps:
            ret += f'{territory["name"]} of {territory["owner"].name} occupied by {territory["troops"]} troops\n'

        return ret

    def join_players(self, player1: str, player2: str, player3: str) -> None:
        self.add_player(player1)
        self.add_player(player2)
        self.add_player(player3)
        self.shuffle_players()

    def avoid_easy_win(self, player: str, this_continent: str, next_territory: str) -> bool:
        territories = 0
        for territory in self.maps:
            if territory["owner"] == player and territory["continent"] == this_continent:
                territories += 1
        if this_continent == "north-america" and territories == 8:
            return False
        elif this_continent == "south-america" and territories == 3:
            return False
        elif this_continent == "europe" and territories == 6:
            return False
        elif this_continent == "africa" and territories == 5:
            return False
        elif this_continent == "asia" and territories == 11:
            return False
        elif this_continent == "oceania" and territories == 3:
            return False
        return True

    def assigning_maps_randomly(self) -> None:
        for player in self.players:
            territories_assigned = 0
            max_territories = 14 #trasformare in costante

            while territories_assigned < max_territories:
                random_num = randint(0, len(self.maps)-1)
                if self.maps[random_num]["owner"] == None:
                    if self.avoid_easy_win(player.name, self.maps[random_num]["continent"], self.maps[random_num]["name"]):
                        self.maps[random_num]["owner"] = player.name
                        self.maps[random_num]["color"] = player.color
                        self.maps[random_num]["troops"] = 1 
                        territories_assigned += 1
    
    def initial_troops_assignment(self, updated_maps) -> None:
        for updated_territory in updated_maps:
            self.maps[self.maps.index(updated_territory)]["troops"] = updated_territory["troops"]

    def has_anyone_won(self) -> str:
        for player in self.players:
            if self.has_a_full_continent(player, player.goal):
                return player
        return None


    def has_a_full_continent(self, player: str, continent: str) -> bool:
        territories = 0
        for territory in self.maps:
            if territory["owner"] == player and territory["continent"] == continent:
                territories += 1
        if continent == "north-america" and territories == 9:
            return True
        elif continent == "south-america" and territories == 4:
            return True
        elif continent == "europe" and territories == 7:
            return True
        elif continent == "africa" and territories == 6:
            return True
        elif continent == "asia" and territories == 12:
            return True
        elif continent == "oceania" and territories == 4:
            return True
        return False

    def from_player_receive_number_of_territories(self, player: str) -> int:
        territories = 0
        for territory in self.maps:
            if territory["owner"] == player:
                territories += 1
        return territories
    
    def __is_territory_owned_by_player(self, territory_name: str, player: Player) -> bool:
        for territory in self.maps:
            if territory["name"] == territory_name and territory["owner"] == player:
                return True
        return False

    def from_territory_name_get_territory_index(self, territory_name: str) -> int:
        for i in range(len(self.maps)):
            if self.maps[i]["name"] == territory_name:
                return i
        return -1

    def add_player(self, player: str, color: str) -> None:
        self.players.append(Player(player, self.possible_goals.pop(randint(0, len(self.possible_goals)-1)), color))
        
        
    def shuffle_players(self) -> None:
        shuffle(self.players)
    


