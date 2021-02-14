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

numbers_indices = []
movement_indices = []

for i in range(2):
    nums = [0,1]
    for game_num in range(1,21):
        # if game_num != 11:
        #     continue
        random.seed(game_num)
        if game_num == 11:
            nums.reverse()
        if i == 0:
            strategy_1 = NumbersBerserkerStrategy(nums[0])
            strategy_2 = AttackBerserkerStrategy(nums[1])
            new_game = Game(invalidation = True, dice_rolls = 'random', logging = False,level = 2, filename = "numbers_attack_level_two_logs.txt")
        elif i == 1:
            strategy_1 = MovementBerserkerStrategy(nums[0])
            strategy_2 = DefenseBerserkerStrategy(nums[1])
            new_game = Game(invalidation = True, logging = False, dice_rolls = 'random', level = 2, filename = "defense_move_level_two_logs.txt")
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
            numbers_indices.append(game_num - 1)
        elif new_game.winner_name == 'move_berserk':
            movement_indices.append(game_num - 1)

print('MOVEMENT', movement_indices)
print('NUMBERS', numbers_indices)