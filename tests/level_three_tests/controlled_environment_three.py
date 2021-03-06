import sys
sys.path.append('src')
from game import Game
from level_three_strategies.numbers_berserker import NumbersBerserkerStrategy
from level_three_strategies.delayed_flanker import DelayedFlankerStrategy
from imported_level_three_strategies.riley import RileyStrategyLevel3
from imported_level_three_strategies.george import GeorgeStrategyLevel3
from imported_level_three_strategies.colby import ColbySiegeStrategyLevel3
from imported_level_three_strategies.david import DavidStrategyLevel3
from imported_level_three_strategies.eli import ElijahStrategyLevel3
from level_three_strategies.justins_wierdo_strategies import BerserkerStrategy
from level_three_strategies.justins_wierdo_strategies import StationaryStrategy
import random
import math

import os
import difflib
import filecmp


berserker = NumbersBerserkerStrategy
eli = ElijahStrategyLevel3
george = GeorgeStrategyLevel3
riley = RileyStrategyLevel3
david = DavidStrategyLevel3
colby = ColbySiegeStrategyLevel3
stationed = StationaryStrategy
berserker_new = BerserkerStrategy

# strats = [colby, george, riley, eli, david, berserker]
# strats = [colby, riley]
bruh = open(os.path.join('logs', 'bruh.txt'), 'a+')
bruh.truncate(0)

def run_game(strategy_1, strategy_2, game_num):
    strategy_1 = strategy_1(1)
    strategy_2 = strategy_2(2)
    random.seed(game_num)
    new_game = Game(invalidation = False, logging = False, dice_rolls = 'random', level = 3, default = False, filename = 'bruh.txt', justin_is_weird = True)
    new_game.add_player(strategy_1, [3,0])
    new_game.add_player(strategy_2, [3,6])
    new_game.initialize_game()
    players = [player.strategy.name for player in new_game.players]
    new_game.run_until_complete()
    return 

winner = run_game(berserker_new, stationed, 5)

# def sort_counts(first_name, second_name, result):
#     if result == first_name:
#         return 'first'
#     elif result == second_name:
#         return 'second'
#     elif result == 'TIE':
#         return 'tie'

# david_wins = []

# for i in range(len(strats)):
#     for j in range(i+1, len(strats)):
#         results = {'first': 0, 'second': 0, 'tie': 0}
#         strats_to_test = [strats[i], strats[j]]
#         matchup = None
#         for _ in range(1):
#             winner = run_game(strats_to_test[0], strats_to_test[1],_+1)
#             first = winner[0][0]
#             second = winner[0][1]
#             result = winner[1]
#             if matchup is None:
#                 matchup = winner[0]
#             if sort_counts(first, second, result) == 'first':
#                 print(_)
#                 david_wins.append(_)
#             results[sort_counts(first, second, result)] += 1
#         strats_to_test.reverse()
#         # for _ in range(50):
#         #     # print(_ + 51)
#         #     winner = run_game(strats_to_test[0], strats_to_test[1],_+51)
#         #     first = winner[0][1]
#         #     second = winner[0][0]
#         #     result = winner[1]
#         #     if sort_counts(first, second, result) == 'first':
#         #         print(_+50)
#         #         david_wins.append(_+50)
#         #     results[sort_counts(first, second, result)] += 1
#         print('-----------------------------------------')
#         print(matchup[0],"VS",matchup[1])
#         print(matchup[0],'WINS:', results['first']/100)
#         print(matchup[1],'WINS:', results['second']/100)
#         print('TIES', results['tie']/100)
#         print('-----------------------------------------')
#         print(david_wins)