import sys
sys.path.append('src')
from player import Player
from units.unit import Unit
from units.scout import Scout
from units.colonyship import Colonyship
from units.colony import Colony
from game import Game
from board import Board
from planet import Planet
from strategies.custom_strategy import CustomStrategy
from strategies.combat_strategy import CombatStrategy
from strategies.dumb_strategy import DumbStrategy

scout_coords = [[0,0], [0,4]]
non_scout_coords = [[2,0], [2,4]]
player_scouts = [3,5,8,10,12]
new_game = Game(logging = False, die_rolls = 'ascending')
strategy_1 = DumbStrategy(player_num = 0)
strategy_2 = DumbStrategy(player_num = 1)
new_game.add_player(strategy_1, [2,0])
new_game.add_player(strategy_2, [2,4])
new_game.initialize_game()

def check_player(player_index, scout_count, turn):
    state = new_game.game_state()
    scouts = [unit['name'] for unit in state['players'][player_index]['units'] if unit['name'] == 'Scout']
    assert len(scouts) == scout_count
    for unit in state['players'][player_index]['units']:
        if unit['name'] == 'Scout':
            if unit['turn created'] == turn:
                assert unit['coords'] == non_scout_coords[player_index]
            else:
                assert unit['coords'] == scout_coords[player_index]
        else:
            assert unit['coords'] == non_scout_coords[player_index]
    print('Passed')

for i in range(4):
    print('===================================')
    new_game.turn_count += 1
    new_game.complete_movement_phase()
    print('Testing',i+1, 'Turn Movement Scouts')
    check_player(0, player_scouts[i], i+1)
    check_player(1, player_scouts[i], i+1)
    print('Testing',i+1, 'Turn Combat Phase')
    new_game.complete_combat_phase()
    print('passed')
    new_game.complete_economic_phase()
    print('Testing',i+1, 'Turn Economic Phase')
    check_player(0, player_scouts[i + 1], i+1)
    check_player(1, player_scouts[i + 1], i+1)
    print('===================================')
