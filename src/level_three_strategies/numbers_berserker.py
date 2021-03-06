class NumbersBerserkerStrategy:

    def __init__(self, player_num):
        self.player_index = player_num
        self.name = 'numbers_berserk'

    def decide_purchases(self, game_state):
        myself = game_state['players'][self.player_index]
        home_coords= game_state['players'][self.player_index]['home_coords']
        purchases = {'units': [], 'technology': []}
        while myself['cp'] >= 6:
            purchases['units'].append({'type': 'Scout', 'coords': home_coords})
            myself['cp'] -= 6
        return purchases

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]
        unit = myself['units'][unit_index]

        home_coords= tuple(hidden_game_state['players'][self.player_index]['home_coords'])
        units = myself['units']
        scouts = [unit for unit in units if unit['type'] == 'Scout' and tuple(unit['coords']) != home_coords]
        num_units = len(scouts)

        # if len(scouts) < 15:
        #     return (0,0)

        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
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

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index