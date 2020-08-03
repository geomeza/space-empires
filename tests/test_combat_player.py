import sys
sys.path.append('src')
from game import Game
import os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def assertion(player,unit_coords):
    for i in range(len(player.units)):
        unit = player.units[i]
        assert unit.coords == unit_coords[i],'Unit at wrong coords'
    print('passed')

g = Game(players = 2, player_coords = [[2,0],[2,4]], grid_size = [5, 5], max_turns = 10,planets = 0,player_type = 'Combat',logging = False)


coords_one = [[2,2],[2,2],[2,2],[2,2],[2,2],[2,2],[2,2]]
coords_two = [[2,2],[2,2],[2,2],[2,2],[2,2],[2,2],[2,2]]
g.start()
g.complete_movement_phase()
enablePrint()
print('Turn One Movement Tests:')
assertion(g.players[0],coords_one)
assertion(g.players[1],coords_two)
blockPrint()
g.complete_combat_phase()
enablePrint()
print('Turn One Combat Test:')
coords_one = [[2,2],[2,2],[2,2]]
assertion(g.players[0], coords_one)