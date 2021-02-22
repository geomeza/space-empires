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
david = DavidStrategyLevel2
eli = ElijahStrategyLevel2
george = GeorgeStrategyLevel2
justin = JustinStrategyLevel2
riley = RileyStrategyLevel2

strats = [berserker, colby, george, riley, eli,david, justin]

def run_game(strategy_1, strategy_2, game_num):
    strategy_1 = strategy_1(0)
    strategy_2 = strategy_2(1)
    random.seed(game_num)
    new_game = Game(invalidation = True, logging = False, dice_rolls = 'random', level = 2, default = False)
    new_game.add_player(strategy_1, [2,0])
    new_game.add_player(strategy_2, [2,4])
    new_game.initialize_game()
    players = [player.strategy.name for player in new_game.players]
    new_game.run_until_complete()
    return [players, new_game.winner_name]

def sort_counts(first_name, second_name, result):
    if result == first_name:
        return 'first'
    elif result == second_name:
        return 'second'
    elif result == 'TIE':
        return 'tie'


for i in range(len(strats)):
    for j in range(i+1, len(strats)):
        results = {'first': 0, 'second': 0, 'tie': 0}
        strats_to_test = [strats[i], strats[j]]
        matchup = None
        for _ in range(250):
            winner = run_game(strats_to_test[0], strats_to_test[1],_+1)
            first = winner[0][0]
            second = winner[0][1]
            result = winner[1]
            if matchup is None:
                matchup = winner[0]
            results[sort_counts(first, second, result)] += 1
        strats_to_test.reverse()
        for _ in range(250):
            winner = run_game(strats_to_test[0], strats_to_test[1],_+251)
            first = winner[0][1]
            second = winner[0][0]
            result = winner[1]
            results[sort_counts(first, second, result)] += 1
        print('-----------------------------------------')
        print(matchup[0],"VS",matchup[1])
        print(matchup[0],'WINS:', results['first']/500)
        print(matchup[1],'WINS:', results['second']/500)
        print('TIES', results['tie']/500)
        print('-----------------------------------------')
        