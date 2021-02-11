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

import os
import difflib
import filecmp
import subprocess as sp


import sys
from logger import Logger

# with open(os.path.join('logs', 'bruh.txt'), 'a+') as f:
#     sys.stdout = f # Change the standard output to the file we created.

new_game = Game(logging=True, die_rolls='random', invalidation=False, scouts_only = False, movement_rounds = 3, screens = False, planets = [[0,2]])
strategy_1 = CustomStrategy(player_num=0)
strategy_2 = NewCustomStrategy(player_num=1)
new_game.add_player(strategy_1, [4, 1])
new_game.add_player(strategy_2, [3, 2])
new_game.initialize_game()

new_game.complete_many_turns(2)
# import sys
# path_to_datasets = 'C:/Users/mezag/Documents/Github/space-empires/'
# filename = 'logs/bruh.txt' 
# filepath = path_to_datasets + filename


# print('This message will be displayed on the screen.')

# original_stdout = sys.stdout # Save a reference to the original standard output

# with open(os.path.join('logs', filename), 'a+') as f:
#     sys.stdout = f # Change the standard output to the file we created.
#     print('This message will be written to a file.')
#     sys.stdout = original_stdout # Reset the standard output to its original value
# throw_file = open(filepath, "w+")
# import io
# import subprocess 

# tester = path_to_datasets + 'tests/level_one_tests/flanker_vs_berserker.py'
# proc = subprocess.Popen(['python',tester],stdout=subprocess.PIPE)
# for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
#     print('huh')
#     throw_file.write(str(line))
# # new_game.run_until_complete()
# print(new_game.complete)

# bruh_dict = {'hello': 5, 'please': 2}
# print(bruh_dict)
# maybe = {'hello': 20, 'bruh': 2}
# bruh_dict.update(maybe)
# print(bruh_dict, maybe)


# class Bruh:
#     bruh_moment = False

#     def __init__(self, **kwargs):
#         self.okay = True
#         self.__dict__.update(kwargs)



# instances = {'bruh_moment': True, 'okay': False, 'hello': '?'}

# # ok = Bruh(**instances)
# ok = Bruh(hello = False, okay = False)

# print(ok.__dict__)
# print(ok.bruh_moment, ok.okay, ok.hello)

# path_to_datasets = 'C:/Users/mezag/Documents/Github/space-empires/logs/'
# filename = 'bruh.txt' 
# filepath = path_to_datasets + filename
# print(filepath)
# throw_file = open(filepath, "w+")

# # print(os.path.join('logs', filename))

# with open(os.path.join('logs', filename), 'a+') as logging_test:
#     for i in range(2):
#         logging_test.write('\n BRUH')

# logger = Logger(filename)

# logger.log('\n HELLO')

# logger.log('\n Bruh Moment')

# logger.log('\n Bruh Moment')
