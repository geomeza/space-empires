class MovementEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game
        self.movement_info = {'1' : [1,1,1,2,2,2], '2': [1,2,2,2,2,3], '3': [1,2,2,2,3,3]}
        self.movement_phase = None


    def complete_movement_phase(self):
        self.game.phase = 'Movement'
        if self.game.logging:
            print('BEGINNING OF MOVEMENT PHASE')
        for i in range(3):
            if self.game.logging:
                print('---------------------------------')
                print('Movement', i + 1)
            self.movement_phase = i+1
            for player in self.game.players:
                movement_lvl = player.tech_lvls['move'] - 1
                movements = self.movement_info[str(i + 1)][movement_lvl]
                if self.game.logging:
                    print('--------------------')
                    print('Player', player.player_num,'is moving')
                self.move_units(player, movements)
                self.board.update(self.game.players)
                if self.game.logging:
                    print('--------------------')
        self.game.combat_engine.colonize()
        self.board.update(self.game.players)
        if self.game.logging:
            print('---------------------------------')
            print('END OF MOVEMENT PHASE')
                

    def move_units(self, player, movements):
        self.game.current_player = player.player_num
        movement_dictionary = player.strategy.decide_ship_movement(self.game.game_state())
        if 'all' in movement_dictionary:
            if 'route' not in movement_dictionary['all']:
                for unit in player.units:
                    if unit.moveable:
                        before_coords = unit.coords
                        for i in range(movements):
                            unit.move(movement_dictionary['all'], self.game.board_size)
                        if self.game.logging:
                            print(unit.name,':',before_coords,'-->',unit.coords)
            else:
                for unit in player.units:
                    if unit.moveable:
                        unit.set_route(movement_dictionary['all']['route'])
                        before_coords = unit.coords
                        for i in range(movements):
                            unit.move(movement_dictionary['all'], self.game.board_size)
                        if self.game.logging:
                            print(unit.name,':',before_coords,'-->',unit.coords)
        else:
            for key,val in movement_dictionary.items():
                if 'route' not in val:
                    for unit in player.units:
                        if unit.name == key:
                            if unit.moveable:
                                before_coords = unit.coords
                                for i in range(movements):
                                    unit.move(movement_dictionary[unit.name], self.game.board_size)
                                if self.game.logging:
                                    print(unit.name,':',before_coords,'-->',unit.coords)
                else:
                    for unit in player.units:
                        if unit.name == key:
                            if unit.moveable:
                                unit.set_route(movement_dictionary[key]['route'])
                                before_coords = unit.coords
                                for i in range(movements):
                                    unit.move(movement_dictionary[key], self.game.board_size)
                                if self.game.logging:
                                    print(unit.name,':',before_coords,'-->',unit.coords)

    
    def generate_movement_state(self):
        movement_dict = {}
        movement_dict['Phase'] = self.movement_phase
        return movement_dict