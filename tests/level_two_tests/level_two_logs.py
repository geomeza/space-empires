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
from level_two_strategies.attack_berserker import AttackBerserkerStrategy
from level_two_strategies.numbers_berserker import NumbersBerserkerStrategy
from level_two_strategies.movement_berserker import MovementBerserkerStrategy
from level_two_strategies.defense_berserker import DefenseBerserkerStrategy
import random
import math
import os

bruh = open(os.path.join('logs', "numbers_attack_level_two_logs.txt"), 'w+')
bruh.truncate()

other_bruh = bruh = open(os.path.join('logs', "defense_move_level_two_logs.txt"), 'w+')
other_bruh.truncate()

attack_wins = 0
movement_wins = 0
defense_wins = 0
numbers_wins = 0

numbers_indices = []
movement_indices = []

for i in range(2):
    nums = [0,1]
    for game_num in range(1,21):
        random.seed(game_num)
        first_few_die_rolls = [math.ceil(10*random.random()) for _ in range(1000)]
        print('first few die rolls of game {}'.format(game_num - 1))
        print('\t',first_few_die_rolls[:7],'\n')
        if game_num == 11:
            nums.reverse()
        if i == 0:
            strategy_1 = AttackBerserkerStrategy(nums[0])
            strategy_2 = NumbersBerserkerStrategy(nums[1])
            # strats = [numbers_strat, attack_strat]
            new_game = Game(invalidation = True, dice_rolls = first_few_die_rolls, logging = False,level = 2, filename = "numbers_attack_level_two_logs.txt")
        elif i == 1:
            strategy_1 = MovementBerserkerStrategy(nums[0])
            strategy_2 = DefenseBerserkerStrategy(nums[1])
            # strats = [movement_strat, defense_strat]
            new_game = Game(invalidation = True, logging = False, dice_rolls = first_few_die_rolls, level = 2, filename = "defense_move_level_two_logs.txt")
        new_game.log('-----------------------------------------------------------------------------------')
        new_game.log('SEED '+ str(game_num)+ ' GAME ' + str(game_num-1))
        new_game.log('-----------------------------------------------------------------------------------')
        if nums[0] == 0:
            new_game.add_player(strategy_1, [2,0])
            new_game.add_player(strategy_2, [2,4])
        if nums[0] == 1:
            new_game.add_player(strategy_2, [2,0])
            new_game.add_player(strategy_1, [2,4])
        new_game.initialize_game()
        new_game.run_until_complete()
        if new_game.winner_name == 'numbers_berserk':
            print('YUHHHHH')
            numbers_indices.append(game_num - 1)
        elif new_game.winner_name == 'move_berserk':
            print('YUHHHHH LMAO')
            movement_indices.append(game_num - 1)

print('MOVEMENT', movement_indices)
print('NUMBERS', numbers_indices)
# for game_num in range(1,21):
#     random.seed(game_num)

#     first_few_die_rolls = [math.ceil(10*random.random()) for _ in range(100)]
#     print('first few die rolls of game {}'.format(game_num - 1))
#     print('\t',first_few_die_rolls[:7],'\n')
#     if game_num== 11:
#         nums.reverse()
#     new_game = Game(planets=[], logging=False, dice_rolls= first_few_die_rolls, invalidation=True, level = 1, filename = "21-02-05-flanker-vs-berserker.txt")
#     new_game.log('-----------------------------------------------------------------------------------')
#     new_game.log('SEED '+ str(game_num)+ 'GAME' + str(game_num-1))
#     new_game.log('-----------------------------------------------------------------------------------')
#     strategy_1 = LevelOneFlankerStrategy(player_num=nums[0])
#     strategy_2 = LevelOneBerserkerStrategy(player_num=nums[1])
#     if nums[0] == 1:
#         print('BERSERKER FIRST')
#         new_game.add_player(strategy_2, [2, 4])
#         new_game.add_player(strategy_1, [2, 0])
#     else:
#         print('FLANKER FIRST')
#         new_game.add_player(strategy_1, [2, 0])
#         new_game.add_player(strategy_2, [2, 4])
#     new_game.initialize_game()
#     # new_game.complete_many_turns(4)
#     new_game.run_until_complete()
#     if new_game.winner_name == 'berserk':
#         berserk_wins += 1
#     else:
#         flankers.append(game_num-1)
#         flanker_wins += 1

# print('Flanker Vs Berserker')
# print('Flanker won', round((flanker_wins/20) * 100,2),'Percent of the matches')
# print('Berserk won', round((berserk_wins/20)* 100,2),'Percent of the matches')
# print(flankers)