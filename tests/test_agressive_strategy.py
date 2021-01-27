import sys
sys.path.append('src')
from player import Player
from units.unit import Unit
from units.scout import Scout
from units.colony_ship import ColonyShip
from units.colony import Colony
from game import Game
from board import Board
from planet import Planet
from strategies.custom_strategy import CustomStrategy
from strategies.combat_strategy import CombatStrategy
from strategies.aggressive_strategy import AggressiveStrategy
from strategies.dumb_strategy import DumbStrategy

# ascending die rolls:
# - num turns: 2
# - num combats: 2
# - winner: Player 0
# - Player 0 ending CP: 7
# - Player 1 ending CP: 7
# descending die rolls:
# - num turns: 2
# - num combats: 2
# - winner: Player 1
# - Player 0 ending CP: 7
# - Player 1 ending CP: 7

print('ASCENDING TESTS')

new_game = Game(logging = True, die_rolls = 'descending')

strategy_1 = AggressiveStrategy(player_num = 0)
strategy_2 = AggressiveStrategy(player_num = 1)

new_game.add_player(strategy_1, [2,0])
new_game.add_player(strategy_2, [2,4])
new_game.initialize_game()
new_game.complete_many_turns(4)