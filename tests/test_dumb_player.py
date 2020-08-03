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
        if unit.name == 'Scout':
            assert unit.coords == unit_coords[i],'Unit at wrong coords'
    print('passed')
g = Game(players = 2, player_coords = [[2,0],[2,4]], grid_size = [5, 5], max_turns = 10,planets = 0,player_type = 'Dumb',logging = False)


coords_one = [[1,0],[1,0],[1,0],[2,0],[2,0],[2,0]]
coords_two = [[1,4],[1,4],[1,4],[2,4],[2,4],[2,4]]
g.start()
g.complete_turn()
enablePrint()
print('Turn One Tests:')
assertion(g.players[0],coords_one,2)
assertion(g.players[1],coords_two,2)
blockPrint()
g.complete_turn()
enablePrint()
print('Turn Two Tests:')
coords_one = [[0,0],[0,0],[0,0],[1,0],[1,0]]
coords_two = [[0,4],[0,4],[0,4],[1,4],[1,4]]
assertion(g.players[0],coords_one,0)
assertion(g.players[1],coords_two,0)
blockPrint()
g.complete_turn()
enablePrint()
print('Turn Three Tests:')
coords_one = [[0,0],[0,0],[0,0],[0,0],[0,0]]
coords_two = [[0,4],[0,4],[0,4],[0,4],[0,4]]
assertion(g.players[0],coords_one,0)
assertion(g.players[1],coords_two,0)
# g.complete_turn()