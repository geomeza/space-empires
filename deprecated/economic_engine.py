class EconomicEngine:

    def __init__(self, board, game, players):
        self.board = board
        self.game = game
        self.players = players

    def economic_state(self, player):
        total_cp = 0
        for colony in player.colonies:
            if colony.colony_type == 'Normal':
                total_cp += colony.capacity
            else:
                total_cp += 20
        maint = 0
        for unit in player.units:
            if unit.name != 'Colony Ship':
                maint += unit.hull_size()
        state = {}
        state.update({'Maintenance': maint})
        state.update({'Income': total_cp})
        return state

    def add_combat_points(self):
        for player in self.players:
            player.generate_cp()

    def pay_maintenance_cost(self):
        for player in self.players:
            player.pay_maintenance()

    def colonize(self, player):
        if player.will_colonize():
            for unit in player.units:
                space = self.board.grid[tuple(unit.coords)]
                if unit.name == 'Colony Ship':
                    if space.planet is not None:
                        if space.planet.colonized is False:
                            space.planet.player = player
                            space.planet.colonized = True
                            unit.destroy()
                            player.create_colony(unit.coords, space.planet, space)

    def update_self(self, players):
        self.players = players

    def complete_economic_phase(self):
        self.game.phase = 'Economic'
        print('----------------------------------')
        print('BEGINNING OF ECONOMIC PHASE')
        self.add_combat_points()
        self.pay_maintenance_cost()
        for player in self.players:
            self.game.current_player = player.player_num - 1
            self.colonize(player)
            print('-----------')
            print('Player',player.player_num,'is upgrading/buying!')
            player.upgrade()
            print('Player',player.player_num,'Combat Points Left:',player.com_points)
            print('-----------')
        print('END OF ECONOMIC PHASE')
        print('----------------------------------')
