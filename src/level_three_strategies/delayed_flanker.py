class DelayedFlankerStrategy:

    def __init__(self, player_num):
        self.player_index = player_num
        self.name = 'delayed_flank'
        self.delayed_count = 0
        self.flank_count = 0
        self.flank_started = False
        self.count_flanks = False
        self.non_flanks = []
        self.turn_count = 1
        self.movement = 1
        self.flank_route_index = 0
        self.flanking_scouts = []
        self.flank_turn = None
        self.behind_direction = {(3,0): (-1,0), (3,6): (1,0)}
        self.flank_route = {(3,0): [(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (1,0), (0,0)],  (3,6): [(0,-1), (0,-1), (0,-1), (0,-1), (0,-1), (0,-1), (-1,0), (0,0)]}

    def decide_purchases(self, game_state):
        myself = game_state['players'][self.player_index]
        home_coords= game_state['players'][self.player_index]['home_coords']
        units = myself['units']
        scouts = [unit for unit in units if unit['type'] == 'Scout']
        num_units = len(scouts)
        attack_level = myself['technology']['attack']
        def_level = myself['technology']['defense']
        game_turn = game_state['turn']
        purchases = {'units': [], 'technology': []}
        if num_units <= 3 and not self.count_flanks:
            if myself['cp'] >= game_state['technology_data']['attack'][attack_level] and attack_level < 2:
                purchases['technology'].append('attack')
                myself['cp'] -= game_state['technology_data']['attack'][attack_level]
            if myself['cp'] >= game_state['technology_data']['defense'][def_level] and def_level < 2:
                purchases['technology'].append('defense')
                myself['cp'] -= game_state['technology_data']['attack'][def_level]
            if attack_level >= 2 and def_level >= 2:
                self.count_flanks = True    
        while myself['cp'] >= 6:
            if num_units >= 3 and not self.count_flanks:
                break
            num_units += 1
            purchases['units'].append({'type': 'Scout', 'coords': home_coords})
            myself['cp'] -= 6
        return purchases

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        home_coords= tuple(hidden_game_state['players'][self.player_index]['home_coords'])
        units = myself['units']
        scouts = [unit for unit in units if unit['type'] == 'Scout' and tuple(unit['coords']) != home_coords]
        num_units = len(scouts)
        game_turn = hidden_game_state['turn']
        game_round = hidden_game_state['round']
        if game_turn != self.turn_count or self.movement != game_round:
            if self.flank_started and self.flank_route_index < 7:
                self.flank_route_index +=1
            self.turn_count = game_turn
            self.movement = game_round
            self.delayed_count = 0
        if self.flank_started and num_units == 0:
            self.flanking_scouts = []
            self.flank_route_index = 0
            self.flank_started= False
            self.flank_count = 0

        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]
       
        unit = myself['units'][unit_index]
        turn_created = unit['turn_created']
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
        if num_units <= 9 and not self.count_flanks:
            return (0,0)

        if unit['type'] == 'Scout' and self.delayed_count < 9 and tuple(unit['coords']) == home_coords:
            self.delayed_count += 1
            if self.flank_started and unit['unit_num'] in self.non_flanks:
                return self.rush(unit_index, hidden_game_state)
            return (0,0)
        elif self.delayed_count < 9 and self.flank_started and unit['unit_num'] not in self.flanking_scouts:
            if tuple(unit['coords']) != home_coords and unit['unit_num'] in self.non_flanks:
                self.delayed_count += 1
                return self.rush(unit_index, hidden_game_state)
            else:
                return (0,0)
        elif self.delayed_count >= 9 or self.flank_started:
            if tuple(unit['coords']) == home_coords:
                if self.flank_started:
                    return (0,0)
                self.flank_count += 1
                return self.behind_direction[home_coords]
            if self.flank_count >= 6:
                if not self.flank_turn:
                    self.flanking_scouts = self.return_scouts(unit['coords'])
                    self.non_flanks = self.return_scouts(home_coords)
                    self.flank_started = True
                return self.flank_route[home_coords][self.flank_route_index]
            else:
                return (0,0)
        else:
            return (0,0)

    def return_scouts(self, coords, game_state):
        myself = hidden_game_state['players'][self.player_index]
        home_coords= tuple(hidden_game_state['players'][self.player_index]['home_coords'])
        units = myself['units']
        return [unit for unit in units if tuple(unit['coords']) == coords]

    def rush(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]
        unit = myself['units'][unit_index]
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
