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
from level_one_strategies.level_one_berserker import LevelOneBerserkerStrategy
from level_one_strategies.level_one_dumb import LevelOneDumbStrategy
from level_one_strategies.level_one_random import LevelOneRandomStrategy
from level_one_strategies.level_one_george import LevelOneGeorgeStrategy
from level_one_strategies.level_one_flanker import LevelOneFlankerStrategy
import random
import math
import os

bruh = open(os.path.join('logs', "21-02-05-flanker-vs-berserker.txt"), 'w')
bruh.truncate()

flanker_wins = 0
berserk_wins = 0
flankers = []
nums = [0,1]
for game_num in range(1,21):
    random.seed(game_num)

    first_few_die_rolls = [math.ceil(10*random.random()) for _ in range(100)]
    print('first few die rolls of game {}'.format(game_num - 1))
    print('\t',first_few_die_rolls[:7],'\n')
    if game_num== 11:
        nums.reverse()
    new_game = Game(planets=[], logging=False, dice_rolls= first_few_die_rolls, invalidation=True, level = 1, filename = "21-02-05-flanker-vs-berserker.txt")
    new_game.log('-----------------------------------------------------------------------------------')
    new_game.log('SEED '+ str(game_num)+ 'GAME' + str(game_num-1))
    new_game.log('-----------------------------------------------------------------------------------')
    strategy_1 = LevelOneFlankerStrategy(player_num=nums[0])
    strategy_2 = LevelOneBerserkerStrategy(player_num=nums[1])
    if nums[0] == 1:
        print('BERSERKER FIRST')
        new_game.add_player(strategy_2, [2, 4])
        new_game.add_player(strategy_1, [2, 0])
    else:
        print('FLANKER FIRST')
        new_game.add_player(strategy_1, [2, 0])
        new_game.add_player(strategy_2, [2, 4])
    new_game.initialize_game()
    # new_game.complete_many_turns(4)
    new_game.run_until_complete()
    if new_game.winner_name == 'berserk':
        berserk_wins += 1
    else:
        flankers.append(game_num-1)
        flanker_wins += 1

print('Flanker Vs Berserker')
print('Flanker won', round((flanker_wins/20) * 100,2),'Percent of the matches')
print('Berserk won', round((berserk_wins/20)* 100,2),'Percent of the matches')
print(flankers)