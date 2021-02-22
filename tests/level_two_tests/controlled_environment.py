import sys
sys.path.append('src')
from game import Game
from level_two_strategies.numbers_berserker import NumbersBerserkerStrategy
from imported_level_two_strategies.colby_strategy import ColbyStrategyLevel2
from imported_level_two_strategies.david_strategy import DavidStrategyLevel2
from imported_level_two_strategies.elijah_strategy import ElijahStrategyLevel2
from imported_level_two_strategies.george_strategy import GeorgeStrategyLevel2
from imported_level_two_strategies.justin_strategy import JustinStrategyLevel2
from imported_level_two_strategies.riley_strategy import RileyStrategyLevel2
import random
import math


berserker = NumbersBerserkerStrategy
colby = ColbyStrategyLevel2
# david = DavidStrategyLevel2
eli = ElijahStrategyLevel2
george = GeorgeStrategyLevel2
justin = JustinStrategyLevel2
riley = RileyStrategyLevel2

strats = [berserker, colby, eli, george, justin, riley]

def run_game(strategy_1, strategy_2, game_num):
    strategy_1 = strategy_1(0)
    strategy_2 = strategy_2(1)
    random.seed(game_num)
    new_game = Game(invalidation = True, logging = True, dice_rolls = 'random', level = 2, default = False, max_turns = 8)
    new_game.add_player(strategy_1, [2,0])
    new_game.add_player(strategy_2, [2,4])
    new_game.initialize_game()
    players = [player.strategy.name for player in new_game.players]
    new_game.run_until_complete()
    return [players, new_game.winner_name]


run_game(berserker, george,1)