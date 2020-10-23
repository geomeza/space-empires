# from units.unit import Unit
# from players.combat_player import CombatPlayer
# from units.colony import Colony
# from board_space import BoardSpace
# from planets.planet import Planet

import sys,os

# Disable
def block_print():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enable_print():
    sys.stdout = sys.__stdout__

from game import Game
block_print()
g = Game(players = 2, player_coords = [[0,0],[4,4]], grid_size = [5, 5], max_turns = 500,planets = 8, player_type = 'Combat', die_rolls = None)
g.start()

for i in range(4):
    enable_print()
    print('TURN ',i+1)  
    g.movement_engine.players = g.players
    print('-----------------------------------') 
    block_print()
    g.movement_engine.complete_first_movement()
    enable_print()
    print(g.movement_engine.generate_movement_state())
    block_print()
    g.movement_engine.complete_second_movement()
    enable_print()
    print(g.movement_engine.generate_movement_state())
    block_print()
    g.movement_engine.complete_third_movement()
    enable_print()
    print(g.movement_engine.generate_movement_state())
    # print(g.find_combat_array())
    print('-----------------------------------') 
# g.complete_movement_phase()
# g.complete_combat_phase()
# g.run_to_completion()
# g.winner()
