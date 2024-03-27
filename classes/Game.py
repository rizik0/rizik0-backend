from classes.Player import Player
from random import shuffle, randint
import uuid

class Game:

    def __init__(self) -> None:
        self.game_id = str(uuid.uuid4())
        self.possible_goals = ["north-america", "south-america", "europe", "africa", "asia", "oceania"]
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

    
    def __str__(self) -> None:
        ret = "Players:\n"
        for player in self.players:
            ret += str(player) + "\n"
        ret += "Map:\n"
        for territory in self.map:
            ret += f'{territory["name"]} of {territory["owner"].name} occupied by {territory["troops"]} troops\n'

        return ret


    def match(self) -> None:
        self.status = "Game is running..."
        
        turn = 0
        while True:
            for player in self.players:
                print(f"Player: {player.name} turn {turn}")

                # Phase 1: Receiving troops
                receiving_troops = int(self.__from_player_receive_number_of_territories(player)/3)

                if (turn != 0 and turn % 3 == 0):
                    receiving_troops += randint(8, 12) # BONUS!

                print("Player: ", player.name, " received ", receiving_troops, " troops")

                # Phase 2: Assigning troops    
                while receiving_troops > 0:
                    territory = input("Choose a territory to send troops: ")
                    if self.__is_territory_owned_by_player(territory, player):
                        self.map[self.__from_territory_name_get_territory_index(territory)]["troops"] += 1
                        receiving_troops -= 1
                    else:
                        print("This is not yours...")
                

                # Phase 3: Attacking
                while True:
                    while True:
                        attacking_territory = input("Choose a territory to attack from: ")
                        if self.__is_territory_owned_by_player(attacking_territory, player):
                            break
                        print("This is not yours...")

                    while True:
                        defending_territory = input("Choose a territory to attack: ")
                        if not self.__is_territory_owned_by_player(defending_territory, player):
                            break
                        print("You can't attack yourself...")
                        if defending_territory in self.map[self.__from_territory_name_get_territory_index(attacking_territory)]["neighbours"]:
                            break
                        print("You can't attack a territory that is not a neighbour...")
                    
                    print("Attacking ", defending_territory, " from ", attacking_territory)

                    attacking_troops = int(input("How many troops are you sending? "))
                    if attacking_troops > self.map[self.__from_territory_name_get_territory_index(attacking_territory)]["troops"] - 1:
                        print("You can't send more troops than you have...")
                        attacking_troops = self.map[self.__from_territory_name_get_territory_index(attacking_territory)]["troops"] - 1
                    elif attacking_troops > 3:
                        print("You can't send more than 3 troops...")
                        attacking_troops = 3
                    elif attacking_troops < 1:
                        print("You can't send less than 1 troop...")
                        attacking_troops = 1
                    
                    defending_troops = self.map[self.__from_territory_name_get_territory_index(defending_territory)]["troops"]
                    if defending_troops > 3:
                        defending_troops = 3
                    
                    attacking_dice = []
                    for i in range(attacking_troops):
                        attacking_dice.append(randint(1, 6))
                        attacking_dice.sort(reverse=True)

                    defending_dice = []
                    for i in range(defending_troops):
                        defending_dice.append(randint(1, 6))
                        defending_dice.sort(reverse=True)

                    attacking_losses = 0
                    defending_losses = 0

                    for i in range(min(attacking_troops, defending_troops)):
                        if attacking_dice[i] > defending_dice[i]:
                            defending_losses += 1
                        else:
                            attacking_losses += 1
                    
                    print("Attacking losses: ", attacking_losses)
                    print("Defending losses: ", defending_losses)

                    self.map[self.__from_territory_name_get_territory_index(attacking_territory)]["troops"] -= attacking_losses
                    self.map[self.__from_territory_name_get_territory_index(defending_territory)]["troops"] -= defending_losses

                    if self.map[self.__from_territory_name_get_territory_index(defending_territory)]["troops"] == 0:
                        print("You won the territory!")
                        self.map[self.__from_territory_name_get_territory_index(defending_territory)]["owner"] = player
                        self.map[self.__from_territory_name_get_territory_index(defending_territory)]["troops"] = attacking_troops
                        self.map[self.__from_territory_name_get_territory_index(attacking_territory)]["troops"] -= attacking_troops

                    print(self)

                    if self.__has_anyone_won() != None:
                        print("Player " + self.__has_anyone_won().name + " has won the game!")
                        break

                    if input("Do you want to attack again? (y/n) ") == "n":
                        break


                # Phase 4: Moving troops
                while True:
                    from_territory = input("Choose a territory to move troops from: ")
                    if self.__is_territory_owned_by_player(from_territory, player):
                        break
                    print("This is not yours...")
                
                while True:
                    to_territory = input("Choose a territory to move troops to: ")
                    if self.__is_territory_owned_by_player(to_territory, player):
                        break
                    print("This is not yours...")
                
                troops_to_move = int(input("How many troops do you want to move? "))
                if troops_to_move > self.map[self.__from_territory_name_get_territory_index(from_territory)]["troops"] - 1:
                    print("You can't move more troops than you have...")
                    troops_to_move = self.map[self.__from_territory_name_get_territory_index(from_territory)]["troops"] - 1
                elif troops_to_move < 1:
                    print("You can't move less than 1 troop...")
                    troops_to_move = 1

                self.map[self.__from_territory_name_get_territory_index(from_territory)]["troops"] -= troops_to_move
                self.map[self.__from_territory_name_get_territory_index(to_territory)]["troops"] += troops_to_move

                print(player.name + " has finished his turn")

                print("--------- UPDATED MAP ---------")
                print(self)

            turn += 1
            

        
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
    
    def initial_troops_assignment(self, updated_map) -> None:
        for updated_territory in updated_map:
            self.map[self.map.index(updated_territory)]["troops"] = updated_territory["troops"]

    def __has_anyone_won(self) -> Player:
        for player in self.players:
            if self.__has_a_full_continent(player, player.goal):
                return player
        return None


    def __has_a_full_continent(self, player: Player, continent: str) -> bool:
        territories = 0
        for territory in self.map:
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

    def __from_player_receive_number_of_territories(self, player: Player) -> int:
        territories = 0
        for territory in self.map:
            if territory["owner"] == player:
                territories += 1
        return territories
    
    def __is_territory_owned_by_player(self, territory_name: str, player: Player) -> bool:
        for territory in self.map:
            if territory["name"] == territory_name and territory["owner"] == player:
                return True
        return False

    def __from_territory_name_get_territory_index(self, territory_name: str) -> int:
        for i in range(len(self.map)):
            if self.map[i]["name"] == territory_name:
                return i
        return -1

    def add_player(self, player: str) -> None:
        self.players.append(Player(player, self.possible_goals.pop(randint(0, len(self.possible_goals)-1))))
        
        
    def shuffle_players(self) -> None:
        shuffle(self.players)
    


