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
        self.game.log('BEGINNING OF ECONOMIC PHASE')
        self.game.log('----------------------------')
        for player in self.game.players:
            self.current_player = player
            income = player.get_income(economic_phase = True)
            player.recieve(income)
            self.game.log('--------------')
            self.game.log('Added '+ str(income)+
                    ' Combat Points from Colonies to Player '+ str(player.player_num))
            self.game.log('New Total: '+ str(player.cp))
            self.game.log('--------------')
            maintenance = player.get_maintenance()
            if player.cp < maintenance:
                removal_cutoff = maintenance - player.cp
                while removal_cutoff > 0:
                    removal = self.remove_ship(player)
                    removal_cutoff -= removal
                maintenance = player.get_maintenance()
            player.pay(maintenance)
            self.game.log('Player '+ str(player.player_num) + ' payed '+
                    str(maintenance)+ ' in maintenance!')
            self.purchase(player)
            player.set_colony_builders()
            player.reset_shipyard_buying_stat()
            self.game.log('PLAYER '+ str(player.player_num) + ' HAS '+ str(player.cp)+ ' LEFT')
            self.board.update(self.game.players)
        self.board.update(self.game.players)
        self.game.log('----------------------------')
        self.game.log('END OF ECONOMIC PHASE')

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
                    if builder is not False:
                        self.game.log('PLAYER '+ str(player.player_num)+
                              ' BOUGHT A: '+ str(ship.name))
            else:
                if self.game.logging:
                    print('Could not afford to buy', ship.name)

    def remove_ship(self, player):
        removal = player.strategy.decide_removal(self.game.hidden_game_state(player.player_num))
        unit = player.units[removal]
        cp = unit.maint
        self.game.log('-------')
        self.game.log('Unit: '+ unit.name+ ' '+str(unit.unit_num)+
                ' could not be sustained, was destroyed!')
        self.game.log('-------')
        unit.destroy()
        return cp

    def economic_state(self):
        return [{
            'player': player.player_num,
            'maintenance cost': player.get_maintenance(),
            'income': player.get_income()
        } for player in self.game.players]
