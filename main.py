from classes.Player import Player
from classes.Game import Game
#from classes.GameStatus import *



game=Game()
game.join_players("player1", "player2", "player3")
game.assigning_map_randomly()
game.print_map()