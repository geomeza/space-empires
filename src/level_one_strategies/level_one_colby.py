import sys
sys.path.append('src')
import random
from imported_strategies.basic_strategy import BasicStrategy

class LevelOneColbyStrategy(BasicStrategy):
    def __init__(self, player_num):  # wutever else we need):
        self.player_index = player_num
        self.name = 'colby'
        self.previous_buy = 'Scout'

    def decide_purchases(self, game_state):
        purchases = {'units': [], 'technology': []}
        total_cost = 0
        while game_state['players'][self.player_index]['cp'] > total_cost:
            if game_state['turn'] == 0 and game_state['players'][self.player_index]['technology']['shipsize'] == 1 and 'shipsize' not in purchases['technology']:
                if game_state['players'][self.player_index]['cp'] > total_cost + self.upgrade_costs('shipsize', game_state):
                    purchases['technology'].append('shipsize')
                    total_cost += self.upgrade_costs('shipsize', game_state)
                else:
                    break
            else:
                ship = self.decide_ship_purchases(game_state)
                if game_state['players'][self.player_index]['cp'] > total_cost + self.ship_cost(ship, game_state):
                    purchases['units'].append(
                        {'type': ship, 'coords': game_state['players'][self.player_index]['home_coords']})
                    total_cost += self.ship_cost(ship, game_state)
                else:
                    break
        return purchases

    def ship_cost(self, ship, game_state):
        return game_state['unit_data'][ship]['cp_cost']

    def decide_ship_purchases(self, game_state):
        if self.check_previous_buy() == 'Destroyer':
            self.previous_buy = 'Scout'
            return 'Scout'
        if self.check_previous_buy() == 'Scout':
            self.previous_buy = 'Destroyer'
            return 'Destroyer'

    def check_previous_buy(self):
        if self.previous_buy == 'Scout':
            return 'Scout'
        elif self.previous_buy == 'Destroyer':
            return 'Destroyer'

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
        if unit_index == 1 and hidden_game_state['turn'] == 0:
            return (-1,0)
        elif unit_index == 1 and hidden_game_state['turn'] > 0 and hidden_game_state['players'][self.player_index]['units'][unit_index]['coords'][1] < 4:
            return (0,1)
        elif unit_index == 1 and hidden_game_state['players'][self.player_index]['units'][unit_index]['coords'][1] == 4 and hidden_game_state['players'][self.player_index]['units'][unit_index]['coords'][0] == 1:
            return (1,0)
        else:
            translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
            best_translation = (0,0)
            smallest_distance_to_opponent = 999999999999
            for translation in translations:
                delta_x, delta_y = translation
                x = x_unit + delta_x
                y = x_unit + delta_y
                dist = abs(x - x_opp) + abs(y - y_opp)
                if dist < smallest_distance_to_opponent:
                    best_translation = translation
                    smallest_distance_to_opponent = dist
            return best_translation