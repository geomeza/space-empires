import random

class LevelOneRandomStrategy:

    def __init__(self, player_num):
        self.player_num = player_num
        self.name = 'random'

    def decide_ship_movement(self, ship_index, game_state):
        x,y = game_state['players'][self.player_num]['units'][ship_index]['coords']
        possible_moves = [[1, 0],[-1, 0],[0, 1],[0, -1],[0,0]]
        choice = random.choice(possible_moves)
        if self.is_in_bounds(x+choice[0], y+choice[1], game_state['board_size']):
            return tuple(choice)
        else:
            return (0,0)

    def is_in_bounds(self, x, y, bounds):
        x1, y1 = bounds
        return (x >= 0 and x < x1) and (y >= 0 and y < y1)

    def decide_removal(self, game_state):
        return -1
        
    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        for unit in combat_state[tuple(location)]:
            if unit['player_index'] != combat_state[tuple(location)][attacker_index]['player_index']:
                return combat_state[tuple(location)].index(unit)