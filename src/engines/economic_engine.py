from units.unit import Unit
from units.scout import Scout
from units.colony_ship import ColonyShip
from units.destroyer import Destroyer
from units.battleship import Battleship
from units.cruiser import Cruiser
from units.dreadnaught import Dreadnaught
from units.ship_yard import ShipYard
from units.decoy import Decoy


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
                print('Added', income,
                      'Combat Points from Colonies to Player', player.player_num)
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
                print('Player', player.player_num, 'payed',
                      maintenance, 'in maintenance!')
            self.purchase(player)
            player.set_colony_builders()
            player.reset_shipyard_buying_stat()
            if self.game.logging:
                print('PLAYER', player.player_num, 'HAS', player.cp, 'LEFT')
            self.board.update(self.game.players)
        self.board.update(self.game.players)
        if self.game.logging:
            print('----------------------------')
            print('END OF ECONOMIC PHASE')

    def purchase(self, player):
        purchases = player.strategy.decide_purchases(self.game.hidden_game_state(player.player_num))
        ship_objects = [Scout, Destroyer, Dreadnaught,
                        ColonyShip, Cruiser, Battleship, ShipYard, Decoy]
        ship_names = ['Scout', 'Destroyer', 'Dreadnaught',
                      'Colonyship', 'Cruiser', 'Battleship', 'Shipyard', 'Decoy']
        for technology in purchases['technology']:
            translations = ['ss', 'atk', 'def', 'move', 'shpyrd']
            techs = ['shipsize', 'attack', 'defense', 'movement', 'shipyard']
            wanted = translations[techs.index(technology)]
            self.game.utility.buy_tech(wanted, player)
        for unit in purchases['units']:
            ship = ship_objects[ship_names.index(unit['type'])]
            if ship.cost <= player.cp:
                ship_coords = [unit['coords'][0], unit['coords'][1]]
                coords = player.check_colony(ship.hull_size, ship, ship_coords)
                if coords is not None:
                    builder = player.build_unit(ship, coords, pay=True)
                    if self.game.logging and builder is not False:
                        print('PLAYER', player.player_num,
                              'BOUGHT A:', ship.name)
            else:
                if self.game.logging:
                    print('Could not afford to buy', ship.name)

    def remove_ship(self, player):
        removal = player.strategy.decide_removal(self.game.hidden_game_state(player.player_num))
        unit = player.units[removal]
        cp = unit.maint
        if self.game.logging:
            print('-------')
            print('Unit:', unit.name, unit.unit_num,
                  'could not be sustained, was destroyed!')
            print('-------')
        unit.destroy()
        return cp

    def economic_state(self):
        return [{
            'player': player.player_num,
            'maintenance cost': player.get_maintenance(),
            'income': player.get_income()
        } for player in self.game.players]
