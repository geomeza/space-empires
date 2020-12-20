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

new_game = Game(logging = True, die_rolls = 'ascending')
strategy_1 = CombatStrategy(player_num = 0)
strategy_2 = CombatStrategy(player_num = 1)
new_game.add_player(strategy_1, [0,0])
new_game.add_player(strategy_2, [4,4])
new_game.initialize_game()
new_game.complete_many_turns(4)

