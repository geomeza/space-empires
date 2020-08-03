# from units.unit import Unit
# from players.combat_player import CombatPlayer
# from units.colony import Colony
# from board_space import BoardSpace
# from planets.planet import Planet

from game import Game

g = Game(players = 2, player_coords = [[2,0],[2,4]], grid_size = [5, 5], max_turns = 500,planets = 0, player_type = 'Combat')
g.start()
g.complete_many_turns(2)
# g.run_to_completion()
# g.winner()
