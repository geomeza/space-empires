import sys
sys.path.append('src')
import random
import math


class BasicStrategy:  # no movement or actual strategy, just funcitons like decide_removal or decide_which_unit_to_attack
    def __init__(self, player_index):
        self.player_index = player_index

    def decide_removal(self, hidden_game_state): #remove weakest 
        return -1

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        return next(index for index, ship in enumerate(combat_state[coords]) if self.player_index != ship['player'])

    def decide_which_units_to_screen(self, hidden_game_state_for_combat):
        return []
                    
    def decide_ship_movement(self, unit_index, game_state):
        return (0,0)

    def will_colonize_planet(self, coordinates, game_state):
        return False

    def upgrade_costs(self, stat_to_upgrade, game_state):
        return game_state['technology_data'][stat_to_upgrade][game_state['players'][self.player_index]['technology'][stat_to_upgrade]]

    def ship_cost(self, ship, game_state):
        return game_state['unit_data'][ship]['cp_cost']

    def get_movement_tech(self, ship_movement_level):
        if ship_movement_level == 1:
            return [1,1,1]
        elif ship_movement_level == 2:
            return [1,1,2]
        elif ship_movement_level == 3:
            return [1,2,2]
        elif ship_movement_level == 4:
            return [2,2,2]
        elif ship_movement_level == 5:
            return [2,2,3]
        elif ship_movement_level == 5:
            return [2,3,3]

    
class ColbySiegeStrategyLevel3(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.name = 'Colby'
        self.combat_has_happend = [False, -6858547829874170]
        self.WE_SIEGIN_BOI = False
        self.DIE_DIE_DIE = False

    def decide_purchases(self, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        enemy = hidden_game_state['players'][1 - self.player_index]
        ships = [ship['coords'] in [enemy['home_coords'], (4, enemy['home_coords'][1]), (2, enemy['home_coords'][1]), (3, enemy['home_coords'][1] + 1), (3, enemy['home_coords'][1] - 1)] for ship in hidden_game_state['players'][self.player_index]['units']]
        if ships.count(True) > 3:
            self.WE_SIEGIN_BOI = True
        elif ships.count(True) > 20:
            self.WE_SIEGIN_BOI = False
            self.DIE_DIE_DIE = True
        else:
            self.WE_SIEGIN_BOI = False
            self.DIE_DIE_DIE = False
        closest_x = min([unit['coords'][0] for unit in hidden_game_state['players'][1 - self.player_index]['units']])
        closest_y = min([unit['coords'][1] for unit in hidden_game_state['players'][1 - self.player_index]['units']])
        def get_distance_to(friendly_unit_coords, enemy_unit_coords):
            return math.sqrt((friendly_unit_coords[0] - enemy_unit_coords[0]) ** 2 + (friendly_unit_coords[1] - enemy_unit_coords[1]) ** 2)
        self.home_coords = hidden_game_state['players'][self.player_index]['home_coords']
        closest_ship = min([unit for unit in hidden_game_state['players'][1 - self.player_index]['units']], key = lambda unit: get_distance_to(self.home_coords, unit['coords']))
        if self.WE_SIEGIN_BOI:
            if hidden_game_state['players'][self.player_index]['cp'] > 100:
                self.WE_SIEGIN_BOI = False
                self.DIE_DIE_DIE = True
            return {'units': [], 'technology': []}
        if get_distance_to(self.home_coords, closest_ship['coords']) > 3 and hidden_game_state['turn'] < 16:
            self.technology = hidden_game_state['players'][self.player_index]['technology']
            purchases = [self.get_technological_purchases('defense', hidden_game_state), self.get_technological_purchases('attack', hidden_game_state)]
            return max(purchases, key=lambda purchase: len(purchase['technology']))
        else:
            purchases = {'units': [], 'technology': []}
            total_cost = 0
            ship = self.choose_ship(purchases, total_cost, hidden_game_state)
            ship_cost = self.ship_cost(ship, hidden_game_state)
            creds = hidden_game_state['players'][self.player_index]['cp']
            while hidden_game_state['players'][self.player_index]['cp'] >= total_cost + self.ship_cost(ship, hidden_game_state):
                purchases['units'].append({'type': ship, 'coords': hidden_game_state['players'][self.player_index]['home_coords']})
                total_cost += self.ship_cost(ship, hidden_game_state)
                ship = self.choose_ship(purchases, total_cost, hidden_game_state)
            return purchases

    def get_technological_purchases(self, stat_to_upgrade, hidden_game_state):
        purchases = {'units': [], 'technology': []}
        while hidden_game_state['players'][self.player_index]['technology'][stat_to_upgrade] + len(purchases['technology']) < 3 and hidden_game_state['technology_data'][stat_to_upgrade][self.technology[stat_to_upgrade] + len(purchases['technology'])] <= hidden_game_state['players'][self.player_index]['cp']:
            purchases['technology'].append(stat_to_upgrade)
            #print("purchase", purchases)
            #print("hidden_game_state['technology_data'][stat_to_upgrade]", hidden_game_state['technology_data'][stat_to_upgrade])
            #print("self.technology[stat_to_upgrade] + len(purchases['technology'])", self.technology[stat_to_upgrade] + len(purchases['technology']))
        return purchases

    def choose_ship(self, purchases, total_cost, hidden_game_state):
        return 'Scout'
        #possible_ships = ['Scout', 'Destroyer', 'Cruiser', 'Battlecruiser', 'Battleship', 'Dreadnaught']
        #return max([ship for ship in possible_ships if self.ship_cost(ship, hidden_game_state) < hidden_game_state['players'][self.player_index]['cp']] - total_cost, key = lambda ship: (ship.fighting_class, -ship.player.player_index, -ship.ID), reverse=True)

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        enemy = hidden_game_state['players'][1 - self.player_index]
        friendly_unit = myself['units'][unit_index]
        self.home_base = myself['units'][0]
        def get_distance_to(friendly_unit_coords, enemy_unit_coords):
            return math.sqrt((friendly_unit_coords[0] - enemy_unit_coords[0]) ** 2 + (friendly_unit_coords[1] - enemy_unit_coords[1]) ** 2)
        closest_ship_to_current_unit = min([unit for unit in hidden_game_state['players'][1 - self.player_index]['units']], key = lambda unit: get_distance_to(friendly_unit['coords'], unit['coords']))
        if [False if unit['coords'] != enemy['home_coords'] else True for unit in enemy['units']].count(True) > 0: #to counter flank strat
            return self.get_translation(hidden_game_state, friendly_unit, closest_ship_to_current_unit['coords'])
        closest_ship_to_home_world = min([unit for unit in hidden_game_state['players'][1 - self.player_index]['units']], key = lambda unit: get_distance_to(self.home_base['coords'], unit['coords']))
        possible_siege_positions = [(4, enemy['home_coords'][1]), 
                                    (2, enemy['home_coords'][1]), 
                                    (3, enemy['home_coords'][1] + 1),
                                    (3, enemy['home_coords'][1] - 1)]
        
        if self.WE_SIEGIN_BOI and friendly_unit['coords'] not in possible_siege_positions: #to siege
            return self.get_translation(hidden_game_state, friendly_unit, min([(position, get_distance_to(friendly_unit['coords'], position)) for position in possible_siege_positions], key = lambda distance: distance[1])[0])
        elif self.DIE_DIE_DIE: #to kill the enemy after some fun
            return self.get_translation(hidden_game_state, friendly_unit, enemy['home_coords'])
        if get_distance_to(self.home_base['coords'], closest_ship_to_home_world['coords']) > 3 and get_distance_to(friendly_unit['coords'], closest_ship_to_current_unit['coords']) > 3 and hidden_game_state['turn'] < 20:
            if [False if unit['coords'] != enemy['home_coords'] else True for unit in myself['units']].count(True) > 5:
                self.WE_SIEGIN_BOI = True
            return (0,0)
        else:
            if myself['units'][unit_index]['coords'] != closest_ship_to_current_unit['coords']:
                if hidden_game_state['turn'] >= self.combat_has_happend[1] + 5:
                    self.combat_has_happend = [True, hidden_game_state['turn']]
                return self.get_translation(hidden_game_state, friendly_unit, closest_ship_to_current_unit['coords'])
            else:
                return (0,0)
        return (0,0)

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        return next(index for index, ship in enumerate(combat_state[coords]) if self.player_index != ship['player'])


    def get_translation(self, hidden_game_state, unit, target_unit_coords):
        '''
        best_translation = (0,0)
        smallest_distance_to_opponent = 999999999999
        for translation in translations:
            x = unit['coords'][0] + translation[0]
            y = unit['coords'][1] + translation[1]
            dist = abs(unit['coords'][0] + translation[0] - x_opp) + abs(unit['coords'][1] + translation[1] - y_opp)
            if dist < smallest_distance_to_opponent:
                best_translation = (translation, (x, y), dist)
                smallest_distance_to_opponent = dist
        #print("new dist", best_translation[2])        #de
        #print('old coords', unit['coords'])           #bu
        #print("new coords", best_translation[1])      #gg
        #print("enemy coords (", x_opp, y_opp, ')')    #in
        #print("best_translation", best_translation[0])#gu'''
        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
        def get_distance_to(friendly_unit_coords, enemy_unit_coords):
            return math.sqrt((friendly_unit_coords[0] - enemy_unit_coords[0]) ** 2 + (friendly_unit_coords[1] - enemy_unit_coords[1]) ** 2)
        def check_translation(unit, translation):
            return (unit['coords'][0] + translation[0], unit['coords'][1] + translation[1])
        return min([(translation, get_distance_to(check_translation(unit, translation), target_unit_coords)) for translation in translations], key = lambda distance: distance[1])[0] #heheh 1 liner gang also the two codes do the same thing