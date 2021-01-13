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
        for unit in player.units:
            if unit.moveable:
                unit_index = player.units.index(unit)
                before_coords = unit.coords
                for _  in range(movements):
                    unit_direction = player.strategy.decide_ship_movement(unit_index, self.game.game_state())
                    unit_direction = [unit_direction[0], unit_direction[1]]
                    unit.move(unit_direction, self.game.board_size)
                    if self.game.logging:
                        print(unit.name,':',before_coords,'-->',unit.coords)
    
    def generate_movement_state(self):
        movement_dict = {}
        movement_dict['Phase'] = self.movement_phase
        return movement_dict