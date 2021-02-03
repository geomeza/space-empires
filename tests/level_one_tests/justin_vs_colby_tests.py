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
import random
from level_one_strategies.level_one_berserker import LevelOneBerserkerStrategy
from level_one_strategies.level_one_dumb import LevelOneDumbStrategy
from level_one_strategies.level_one_random import LevelOneRandomStrategy
from level_one_strategies.level_one_george import LevelOneGeorgeStrategy
from level_one_strategies.level_one_colby import LevelOneColbyStrategy
from level_one_strategies.level_one_justin_berserker import LevelOneBerserkerStrategy as LevelOneJustinStrategy

colby_wins = 0
justin_wins = 0
for i in range(100):
    new_game = Game(planets=[], logging=False, die_rolls='random', invalidation=True, scouts_only = True, movement_rounds = 1, banned_phases = ['economic'], screens = False)
    nums = random.choice([[0,1], [1,0]])
    # nums = [0,1]
    # if i%2 == 1:
    #     nums.reverse()
    strategy_1 = LevelOneColbyStrategy(player_num=nums[0])
    strategy_2 = LevelOneJustinStrategy(player_num=nums[1])
    if nums[0] == 1:
        new_game.add_player(strategy_2, [2, 4])
        new_game.add_player(strategy_1, [2, 0])
    else:
        new_game.add_player(strategy_1, [2, 0])
        new_game.add_player(strategy_2, [2, 4])
    new_game.initialize_game()
    # new_game.complete_many_turns(4)
    new_game.run_until_complete()
    if new_game.winner_name == 'justin':
        justin_wins += 1
    else:
        colby_wins += 1

print('Justin Berserk won', justin_wins,'Out of 100 matches')
print('Colby won', colby_wins,'Out of 100 matches')