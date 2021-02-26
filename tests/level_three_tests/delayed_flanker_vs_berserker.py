import sys
sys.path.append('src')
from game import Game
from level_three_strategies.numbers_berserker import NumbersBerserkerStrategy
from level_three_strategies.delayed_flanker import DelayedFlankerStrategy
import random
import math


berserker = NumbersBerserkerStrategy
delayed_flanker = DelayedFlankerStrategy

strats = [berserker, delayed_flanker]

def run_game(strategy_1, strategy_2, game_num):
    strategy_1 = strategy_1(0)
    strategy_2 = strategy_2(1)
    random.seed(game_num)
    new_game = Game(invalidation = True, logging = False, dice_rolls = 'random', level = 3, default = False)
    new_game.add_player(strategy_1, [3,0])
    new_game.add_player(strategy_2, [3,6])
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
        for _ in range(500):
            winner = run_game(strats_to_test[0], strats_to_test[1],_+1)
            first = winner[0][0]
            second = winner[0][1]
            result = winner[1]
            if matchup is None:
                matchup = winner[0]
            results[sort_counts(first, second, result)] += 1
        strats_to_test.reverse()
        for _ in range(500):
            winner = run_game(strats_to_test[0], strats_to_test[1],_+51)
            first = winner[0][1]
            second = winner[0][0]
            result = winner[1]
            results[sort_counts(first, second, result)] += 1
        print('-----------------------------------------')
        print(matchup[0],"VS",matchup[1])
        print(matchup[0],'WINS:', results['first']/1000)
        print(matchup[1],'WINS:', results['second']/1000)
        print('TIES', results['tie']/1000)
        print('-----------------------------------------')