class EconomicEngine:

    def __init__(self, board, game):
        self.board = board
        self.game = game
        self.current_player = None


    def complete_economic_phase(self):
        self.game.phase = 'Economic'
        if self.game.logging:
            print('BEGINNING OF ECONOMIC PHASE')
            print('----------------------------')
        for player in self.game.players:
            self.current_player = player
            income = player.get_income()
            player.recieve(income)
            if self.game.logging:
                print('--------------')
                print('Added', income, 'Combat Points from Colonies to Player', player.player_num)
                print('New Total:', player.cp)
                print('--------------')
            maintenance = player.get_maintenance()
            if player.cp < maintenance:
                removal_cutoff = maintenance - player.cp
                while removal_cutoff > 0:
                    removal = self.remove_ship(player)
                    removal_cutoff -= removal
                maintenance = player.get_maintenance()
            player.pay(maintenance)
            if self.game.logging:
                print('Player',player.player_num,'payed',maintenance,'in maintenance!')
            self.purchase(player)
            if self.game.logging:
                print('PLAYER', player.player_num,'HAS', player.cp,'LEFT')
            self.board.update(self.game.players)
        self.board.update(self.game.players)
        if self.game.logging:
            print('----------------------------')
            print('END OF ECONOMIC PHASE')


    def purchase(self, player):
        purchases = player.strategy.decide_purchases(self.game.game_state())
        for key,val in purchases.items():
            if key == 'units':
                for ship in val:
                    if ship.cost <= player.cp:
                        builder = player.build_unit(ship, player.coords_to_build(ship.build_size, ship), pay = True)
                        if self.game.logging and builder is not False:
                            print('PLAYER', player.player_num,'BOUGHT A:', ship.name)
                    else:
                        if self.game.logging:
                            print('Could not afford to buy', ship.name)
            elif key == 'tech':
                for tech_type in val:
                    self.game.utility.buy_tech(tech_type, player)


    def remove_ship(self, player):
        removal = player.strategy.decide_removal(self.game.game_state())
        unit = player.units[removal]
        cp = unit.maint
        if self.game.logging:
            print('-------')
            print('Unit:',unit.name, unit.unit_num,'could not be sustained, was destroyed!')
            print('-------')
        unit.destroy()
        return cp

    def economic_state(self):
        return [{
            'player' : player.player_num,
            'maintenance cost': player.get_maintenance(),
            'income':player.get_income()
        } for player in self.game.players]