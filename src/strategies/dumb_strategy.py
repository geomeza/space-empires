from units.scout import Scout
from units.cruiser import Cruiser
from units.colonyship import Colonyship
from units.colony import Colony
from planet import Planet
from units.shipyard import Shipyard
from units.base import Base
from units.destroyer import Destroyer

class DumbStrategy:

    def __init__(self, player_num):
        self.player_num = player_num

    def decide_ship_movement(self, ship_index, game_state):
        if game_state['players'][self.player_num]['units'][ship_index]['name'] == 'Scout':
            return (-1,0) 
        else:
            return (0,0)

    def decide_purchases(self, game_state):
        purchases = {}
        cp =game_state['players'][self.player_num]['cp']
        units = []
        if cp > Scout.cost:
            while True:
                if cp >= Scout.cost:
                    units.append(Scout)
                    cp -= Scout.cost
                else:
                    break
        if len(units) >= 1:
            purchases['units'] = units
        purchases['tech'] = []
        return purchases

    def decide_removal(self, game_state):
        return -1
        
    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        for unit in combat_state[tuple(location)]:
            if unit['player'] != combat_state[tuple(location)][attacker_index]['player']:
                return combat_state[tuple(location)].index(unit)


    def will_colonize_planet(self, coords, game_state):
        return False

    def decide_which_units_to_screen(self, combat_state):
        return []