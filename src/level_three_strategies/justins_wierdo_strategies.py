class BerserkerStrategy:

    def __init__(self, player_number):
        self.player_number = player_number
        self.name = 'berserk'

    def decide_ship_movement(self, unit_type, unit_num, hidden_game_state):
        units = hidden_game_state['players'][self.player_number]['units']
        for unit in units:
            if unit['type'] == unit_type and unit['num'] == unit_num:
                if unit['coords'] != (3,6):
                    return (0,1)

    def decide_which_unit_to_attack(self, combat_state, game_state, coords, attacker_type, attacker_num):
        # attack the first opposing ship that's not a Homeworld or Colony

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                if unit['type'] not in ['Homeworld', 'Colony']:
                    return (unit['type'], unit['num'])

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                return (unit['type'], unit['num'])

class StationaryStrategy:

    def __init__(self, player_number):
        self.player_number = player_number
        self.name = 'stationary'

    def decide_ship_movement(self, unit_type, unit_num, hidden_game_state):
        return (0,0)

    def decide_which_unit_to_attack(self, combat_state, game_state, coords, attacker_type, attacker_num):
        # attack the first opposing ship that's not a Homeworld or Colony

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                if unit['type'] not in ['Homeworld', 'Colony']:
                    return (unit['type'], unit['num'])

        for unit in combat_state[coords]:
            if unit['player'] != self.player_number:
                return (unit['type'], unit['num'])