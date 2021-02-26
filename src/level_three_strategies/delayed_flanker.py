class DelayedFlankerStrategy:

    def __init__(self, player_num):
        self.player_index = player_num
        self.name = 'delayed_flank'
        self.delayed_count = 0
        self.flank_count = 0
        self.flank_turn = None
        self.turn_count = 1
        self.behind_direction = {(3,0): (-1,0), (3,6): (1,0)}
        self.flank_route = {(3,0): [(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (1,0)],  (3,6): [(0,-1), (0,-1), (0,-1), (0,-1), (0,-1), (-1,0)]}

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
        home_coords= hidden_game_state['players'][self.player_index]['home_coords']
        units = myself['units']
        scouts = [unit for unit in units if unit['type'] == 'Scout']
        num_units = len(scouts)
        game_turn = hidden_game_state['turn']
        if game_turn != self.turn_count:
            self.turn_count = game_turn
            self.delayed_count = 0

        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        turn_created = unit['turn_created']
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
        if unit['type'] == 'Scout' and self.delayed_count < 8 and unit['coords'] == home_coords:
            self.delayed_count += 1
            return (0,0)
        elif self.delayed_count >= 8:
            if unit['coords'] == home_coords:
                self.flank_count += 1
                return self.behind_direction[home_coords]
            if self.flank_count == 15:
                self.flank_turn = game_turn
                return self.flank_route[home_coords][game_turn - self.flank_turn]
            

        
        # translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
        # best_translation = (0,0)
        # smallest_distance_to_opponent = 999999999999
        # for translation in translations:
        #     delta_x, delta_y = translation
        #     x = x_unit + delta_x
        #     y = x_unit + delta_y
        #     dist = abs(x - x_opp) + abs(y - y_opp)
        #     if dist < smallest_distance_to_opponent:
        #         best_translation = translation
        #         smallest_distance_to_opponent = dist
        # return best_translation

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index 
