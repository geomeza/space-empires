import sys
sys.path.append('src')
from Game import Game
g = Game(players = 2, player_coords = [[2,0],[2,4]], combat_points = 50, grid_size = [5, 5], max_turns = 10,planets = 0,dumb_players = True)
g.start()
g.complete_many_turns(10)