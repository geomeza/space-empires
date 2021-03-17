class MovementEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game
        self.movement_info = {'1': [1, 1, 1, 2, 2, 2], '2': [
            1, 2, 2, 2, 2, 3], '3': [1, 2, 2, 2, 3, 3]}
        self.movement_phase = None

    def complete_movement_phase(self):
        if self.game.turn_count != 1:
            self.game.log('\n')
        self.game.log('BEGINNING OF TURN ' +
                      str(self.game.turn_count) + ' MOVEMENT PHASE')
        for player in self.game.players:
            player.reset_movements()
        for i in range(self.game.movement_rounds):
            # self.game.log('---------------------------------')
            self.game.log('\n\tMovement Round ' + str(i + 1))
            self.movement_phase = i+1
            for player in self.game.players:
                # movement_lvl = player.tech_lvls['move'] - 1
                # movements = self.movement_info[str(i + 1)][movement_lvl]
                # self.game.log('--------------------')
                # self.game.log('Player '+ str(player.player_num) + ' is moving')
                self.move_units(player, i+1)
                # self.game.log('--------------------')
        # self.game.combat_engine.colonize()
        self.game.log('\n\tEnding Unit Locations')
        self.game.show_unit_coords()
        self.board.update(self.game.players)
        # self.game.log('---------------------------------')
        self.game.log('END OF TURN ' +
                      str(self.game.turn_count) + ' MOVEMENT PHASE')

    def move_units(self, player, movement_round):
        self.game.current_player = player.player_num
        for unit in player.units:
            if unit.player.dead:
                break
            if unit.moveable:
                ship_movements = self.movement_info[str(
                    movement_round)][unit.movement - 1]
                unit_index = player.units.index(unit)
                before_coords = unit.coords
                for _ in range(ship_movements):
                    unit_direction = player.strategy.decide_ship_movement(
                        unit.name, unit.unit_num, self.game.hidden_game_state(player.player_num))
                    unit_direction = [unit_direction[0], unit_direction[1]]
                    unit.move(unit_direction, self.game.board_size)
                    self.adjust_attacking_vars(unit.coords, unit)
                    self.board.update(self.game.players)
                    self.game.combat_engine.check_occupace(unit.coords)
                    if unit.player.dead:
                        break
                    if unit.name == 'Colonyship':
                        self.game.combat_engine.colonize(unit.coords)
                    if before_coords != unit.coords:
                        self.game.log('\t\tPlayer '+str(unit.player.player_num)+' '+unit.name+' '+str(
                            unit.unit_num) + ': ' + str(tuple(before_coords)) + ' -> ' + str(tuple(unit.coords)))
            # elif unit.brought_into_fight:
            #     self.game.log(unit.name+ str(unit.unit_num) +' : '+ str(unit.coords)+ ' --> '+ str(unit.coords))

    def generate_movement_state(self):
        movement_dict = {}
        movement_dict['Phase'] = self.movement_phase
        return movement_dict

    def reset_attacking_vars(self):
        for player in self.game.players:
            for unit in player.units:
                unit.attacking = False

    def adjust_attacking_vars(self, coords, arriving_unit):
        space_units = self.game.board.get_space_units(coords)
        if arriving_unit in space_units:
            space_units.remove(arriving_unit)
        enems = [unit for unit in space_units if unit.player != arriving_unit.player]
        if len(enems) >= 1:
            arriving_unit.attacking = True

