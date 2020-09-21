# from units.unit import Unit
# from players.combat_player import CombatPlayer
# from units.colony import Colony
# from board_space import BoardSpace
# from planets.planet import Planet

from game import Game

g = Game(players = 2, player_coords = [[2,1],[2,3]], grid_size = [5, 5], max_turns = 500,planets = 12, player_type = 'Combat', die_rolls = 'Descending')
g.start()
g.complete_many_turns(1)
# g.complete_movement_phase()
# g.complete_combat_phase()
# g.run_to_completion()
# g.winner()
