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

flanker_wins = 0
random_wins = 0

for i in range(1000):
    new_game = Game(planets=[], logging=False, die_rolls='random', invalidation=True, scouts_only = True, movement_rounds = 1, banned_phases = ['economic'], screens = False, max_turns = 10, default = True)
    nums = [0,1]
    if i%2 == 1:
        nums.reverse()
    strategy_1 = LevelOneFlankerStrategy(player_num=nums[0])
    strategy_2 = LevelOneRandomStrategy(player_num=nums[1])
    if nums[0] == 1:
        new_game.add_player(strategy_2, [2, 4])
        new_game.add_player(strategy_1, [2, 0])
    else:
        new_game.add_player(strategy_1, [2, 0])
        new_game.add_player(strategy_2, [2, 4])
    new_game.initialize_game()
    # new_game.complete_many_turns(4)
    new_game.run_until_complete()
    if new_game.winner_name == 'random':
        random_wins += 1
    else:
        flanker_wins += 1

print('Flanker Vs Random')
print('Flanker won', (flanker_wins/1000) * 100,'Percent of the matches')
print('Random won', (random_wins/1000)* 100,'Percent of the matches')