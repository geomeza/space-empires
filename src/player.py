from units.scout import Scout
from units.cruiser import Cruiser
from units.colony_ship import ColonyShip
from units.colony import Colony
from units.base import Base
from planet import Planet
from units.ship_yard import ShipYard
# from units.ship_yard import ShipYard


class Player:

    def __init__(self, strategy, player_num, starting_coords, game):
        self.strategy = strategy
        self.player_num = player_num
        self.tech_lvls = {'atk' : 0, 'def' : 0, 'move' : 1, 'shpyrd' : 1, 'ss' : 1}
        self.home_coords = starting_coords
        self.home_planet = None
        self.game = game
        self.units = []
        self.cp = 0
    
    def build_unit(self, unit_name, coords, pay = True):
        colony = self.find_colony(coords)
        if unit_name.name == 'Base':
            if colony.base is not None:
                if self.game.logging:
                    print('Colony Already Has Base')
                return False
        if unit_name.name == 'Shipyard':
            if len(colony.shipyards) == 4:
                if self.game.logging:
                    print('Colony Already Has 4 Shipyards')
                return False
        ship_tech = {key: val for key,val in self.tech_lvls.items() if key in ['atk', 'def', 'move']}
        new_unit = unit_name(coords, len(self.units) + 1, self, ship_tech, self.game, self.game.turn_count)
        if pay:
            self.cp -= new_unit.cost
        self.units.append(new_unit)

    def find_colony(self, coords):
        for unit in self.units:
            if unit.name == 'Colony':
                if unit.coords == coords:
                    return unit

    def build_colony(self, coords, col_type = 'Normal', colony_ship = None):
        ship_tech = {key: val for key,val in self.tech_lvls.items() if key in ['atk', 'def']}
        if col_type == 'Home':
            home_colony = Colony(coords, len(self.units) + 1, self, ship_tech, self.game, self.game.turn_count,colony_type = 'Home')
            self.units.append(home_colony)
        else:
            new_colony = Colony(coords, len(self.units) + 1, self, ship_tech, self.game, self.game.turn_count, colony_type = 'Normal')
            self.game.board.grid[tuple(coords)].planet.colonize(self, new_colony)
            self.units.append(new_colony)
            if colony_ship is not None:
                colony_ship.destroy()

    def initialize_units(self):
        self.build_colony(self.home_coords, col_type = 'Home')
        home_planet = Planet(self.home_coords, colonized = True, colony = self.units[0])
        self.home_planet = home_planet
        self.game.board.planets.append(home_planet)
        self.game.board.grid[tuple(self.home_coords)].planet = home_planet
        for i in range(4):
            self.build_unit(ShipYard, self.home_coords, pay = False)
        self.units[0].set_builders()
        for i in range(3):
            self.build_unit(Scout, self.home_coords, pay = False)
        for i in range(3):
            self.build_unit(ColonyShip, self.home_coords, pay = False)

    def coords_to_build(self, build_size, ship):
        for unit in self.units:
            if unit.name == 'Colony':
                if self.tech_lvls['ss'] >= ship.ship_size_needed:
                    if unit.builders >= build_size:
                        unit.builders -= build_size
                        return unit.coords
                    else:
                        if self.game.logging:
                            print('Player does not have enough builders at colonies to build ship')
                        return None
                else:
                    if self.game.logging:
                        print('Player does not have proper ship size level')
                    return None

    def update_shipyards(self):
        for unit in self.units:
            if unit.name == 'Shipyard':
                unit.build_capacity = self.game.utility.ship_size_dict[str(self.tech_lvls['shpyrd'])]
        self.set_colony_builders()

    def set_colony_builders(self):
        for unit in self.units:
            if unit.name == 'Colony':
                unit.set_builders()

    def pay(self, payment):
        self.cp -= payment
    
    def recieve(self, income):
        self.cp += income

    def get_maintenance(self):
        total_maint = 0
        for unit in self.units:
            if unit.maint is not None:
                total_maint += unit.maint
        return total_maint

    def get_income(self):
        income = 0
        for unit in self.units:
            if unit.name == 'Colony':
                income += unit.capacity
        return income
