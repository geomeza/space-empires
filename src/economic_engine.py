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
                self.remove_ships(player)
                maintenance = self.get_maintenance()
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
        purchases = player.strategy.decide_purchases(self.game.player_state(player))
        for key,val in purchases.items():
            if key == 'ships':
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
                    for i in range(tech_type[1]):
                        self.game.utility.buy_tech(tech_type[0], player)


    def remove_ships(self, player):
        removals = player.strategy.decide_removals(self.game.player_state(player))
        for unit in player.units:
            if self.game.logging:
                print('-------')
                print('Unit:',unit.name, unit.unit_num,'could not be sustained, was destroyed!')
                print('-------')
            if unit.unit_num in removals:
                unit.destroy()

    def economic_state(self):
        return [{
            'player' : player.player_num,
            'maintenance cost': player.get_maintenance(),
            'income':player.get_income()
        } for player in self.game.players]