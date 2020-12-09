from units.scout import Scout
from units.cruiser import Cruiser
from units.colonyship import Colonyship
from units.colony import Colony
from planet import Planet
from units.shipyard import Shipyard
from units.base import Base
from units.destroyer import Destroyer

class CombatStrategy:

    def __init__(self, exist):
        self.exist = True
        self.buy_counter = 0

    def decide_ship_movement(self, game_state):
        # print(game_state)
        return {'all': {'route' : [game_state['board_size'][0]// 2, game_state['board_size'][1]// 2]}}

    def decide_purchases(self, player_state):
        purchases = {}
        cp = player_state['cp']
        units = []
        if player_state['tech']['ss'] < 2:
            purchases['tech'] = [['ss', 1]]
            cp -= 10
        if cp > self.check_buy_counter().cost:
            while True:
                unit = self.check_buy_counter()
                if cp >= unit.cost:
                    units.append(unit)
                    cp -= unit.cost
                    self.buy_counter += 1
                else:
                    break
        if len(units) >= 1:
            purchases['ships'] = units
        return purchases

    def check_buy_counter(self):
        if self.buy_counter % 2 == 0:
            return Destroyer
        else:
            return Scout


    def decide_removals(self, player_state):
        removals = []
        threshold = self.get_maintenance() - self.cp
        for unit in player_state['units']:
            removals.append(unit['unit num'])
            threshold -= unit['maint']
            if threshold <= 0:
                break
        return removals
        
    def decide_which_ship_to_attack(self, attacker, unit_info):
        return unit_info[0]

    def will_colonize(self, colony_ship, game_state):
        return False