from player import Player
from units.unit import Unit
from units.scout import Scout
from units.colony_ship import ColonyShip
from units.colony import Colony
from game import Game
from board import Board
from planet import Planet
from strategies.custom_strategy import CustomStrategy
from strategies.new_custom_strategy import NewCustomStrategy
from strategies.combat_strategy import CombatStrategy
from strategies.dumb_strategy import DumbStrategy

new_game = Game(planets=[], logging=True, die_rolls='random', invalidation=True, scouts_only = True, movement_rounds = 1, banned_phases = ['economic'], screens = False)
strategy_1 = DumbStrategy(player_num=0)
strategy_2 = DumbStrategy(player_num=1)
new_game.add_player(strategy_1, [4, 1])
new_game.add_player(strategy_2, [3, 2])
new_game.initialize_game()

new_game.complete_many_turns(4)
# new_game.run_until_complete()
print(new_game.complete)
