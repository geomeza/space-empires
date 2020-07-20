import sys
sys.path.append('Units')
# from board import Board
# from Units.Unit import Unit

from Game import Game

g = Game(players = 2, player_coords = [[0,0],[2,2]], combat_points = 50, grid_size = [3, 3], max_turns = 50,planets = 1)
g.start()
g.run_to_completion()