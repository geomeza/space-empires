from units.scout import Scout
from units.cruiser import Cruiser
from units.colonyship import Colonyship
from units.colony import Colony
from planet import Planet
from units.shipyard import Shipyard
from units.base import Base

class CustomStrategy:

    def __init__(self, exist):
        self.exist = True

    def decide_ship_movement(self, game_state):
        # print(game_state)
        return {'Scout': [-1,0]}

    def decide_purchases(self, player_state):
        return {'ships': [Shipyard]}

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
        return True