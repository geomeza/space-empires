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

berserk_one_wins = 0
berserk_two_wins = 0

for i in range(100):
    new_game = Game(planets=[], logging=False, die_rolls='random', invalidation=True, scouts_only = True, movement_rounds = 1, banned_phases = ['economic'], screens = False)
    strategy_1 = LevelOneBerserkerStrategy(player_num=0)
    strategy_2 = LevelOneBerserkerStrategy(player_num=1)
    new_game.add_player(strategy_1, [2, 0])
    new_game.add_player(strategy_2, [2, 4])
    new_game.initialize_game()
    # new_game.complete_many_turns(4)
    new_game.run_until_complete()
    if new_game.winner == 1:
        berserk_two_wins += 1
    else:
        berserk_one_wins += 1

print('Berserk one won', berserk_one_wins,'Out of 100 matches')
print('Berserk two won', berserk_two_wins,'Out of 100 matches')