import random

class BasicStrategy:  # no movement or actual strategy, just funcitons like decide_removal or decide_which_unit_to_attack or simple_sort
    def __init__(self, player_index):  # wutever we need):
        self.player_index = player_index

    def decide_removal(self, hidden_game_state):
        return self.simple_sort(hidden_game_state['players'][self.player_index]['units'])[-1]['ID']

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index 

    def decide_which_units_to_screen(self, hidden_game_state_for_combat):
        return []
        
    def simple_sort(self, game_state):
        fixed_arr = []
        for ship_attributes in game_state['players'][self.player_index]['units']:
            if ship_attributes['type'] != 'Decoy' and ship_attributes['type'] != 'Colony Ship' and ship_attributes['type'] != 'Miner' and ship_attributes['type'] != 'Colony':
                fixed_arr.append(ship_attributes)
        sorted_arr = []
        while len(fixed_arr) > 0:
            strongest_ship = max(fixed_arr, key=lambda ship: ship['technology']['tactics'] + ship['technology']['tactics'] + game_state['unit_data'][ship['type']]['attack'])
            sorted_arr.append(strongest_ship)
            fixed_arr.remove(strongest_ship)
        return sorted_arr
                    
    def decide_ship_movement(self, unit_index, game_state):
        ship_yards = game_state['players'][self.player_index]['shipyards']
        
        random_ship_yard = math.floor(len(ship_yards)*random.random()) + 1
        return ship_yards[random_ship_yard]['coords'][0], ship_yards[random_ship_yard]['coords'][1]

    def will_colonize_planet(self, coordinates, game_state):
        return False

    def upgrade_costs(self, stat_to_upgrade, game_state):
        return game_state['technology_data'][stat_to_upgrade][game_state['players'][self.player_index]['technology'][stat_to_upgrade]]

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