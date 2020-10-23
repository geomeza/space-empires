class MovementEngine:

    def __init__(self, game, board):
        self.game = game
        self.board = board
        self.players = None
        self.movement_phase = None

    def complete_movement_phase(self, players):
        self.players = players
        print('BEGINNING OF MOVEMENT PHASE')
        print('-----------------------------------------')
        self.complete_first_movement()
        self.complete_second_movement()
        self.complete_third_movement()
        print('-----------------------------------------')
        print('END OF MOVEMENT PHASE')

    def complete_first_movement(self):
        self.movement_phase = 1
        movements = 0
        print('--------------------------------------')
        print('FIRST MOVEMENT')
        for player in self.players:
            self.current_player = player.player_num - 1
            if player.tech_lvls[2] <= 3:
                movements = 1
            else:
                movements = 2
            print('--------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.game.grid_size, movements)
            print('--------------------------------')
        print('--------------------------------------')

    def complete_second_movement(self):
        self.movement_phase = 2
        movements = 0
        print('--------------------------------------')
        print('SECOND MOVEMENT')
        for player in self.players:
            if player.tech_lvls[2] <= 1:
                movements = 1
            elif player.tech_lvls[2] <= 5:
                movements = 2
            else:
                movements = 3
            print('--------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.game.grid_size, movements)
            print('--------------------------------')
        print('--------------------------------------')

    def complete_third_movement(self):
        self.movement_phase = 3
        movements = 0
        print('--------------------------------------')
        print('THIRD MOVEMENT')
        for player in self.players:
            if player.tech_lvls[2] <= 1:
                movements = 1
            elif player.tech_lvls[2] <= 4:
                movements = 2
            else:
                movements = 3
            print('--------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.game.grid_size, movements)
            print('--------------------------------')
        print('--------------------------------------')

    def generate_movement_state(self):
        movement_dict = {}
        movement_dict['Phase'] = self.movement_phase
        return movement_dict