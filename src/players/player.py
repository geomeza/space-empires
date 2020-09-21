from units.unit import Unit 
from units.dreadnaught import Dreadnaught 
from units.scout import Scout 
from units.battlecruiser import Battlecruiser 
from units.battleship import Battleship 
from units.colony import Colony 
from units.colonyship import Colonyship 
from units.cruiser import Cruiser 
from units.destroyer import Destroyer 
from units.shipyard import Shipyard 
from units.base import Base
from planets.planet import Planet 
import random

class Player:
    def __init__(self, player_num):
        self.tech_lvls = [0, 0, 1, 1, 1]
        self.unit_count = 0
        self.player_type = 'Player'
        self.unit_counter = 0
        self.units = []
        self.com_points = 0
        self.player_num = player_num
        self.coordins = None
        self.colonies = [] 
        self.colony_count = 0
        self.col_counter = 0
        self.shipyard_count = 0
        self.base_count = 0

    def generate_cp(self):
        print('--------------')
        total_cp = 0
        for colony in self.colonies:
            if colony.colony_type == 'Normal':
                total_cp += colony.capacity
            else:
                total_cp += 20
        self.com_points += total_cp
        print('Added', total_cp, 'Combat Points from Colonies to Player', self.player_num)
        print('New Total:',self.com_points)
        print('--------------')

    def pay_maintenance(self):
        print('--------------')
        for unit in self.units:
            if unit.name != 'Colony Ship':
                unit.maint = unit.hull_size
            else:
                continue
            if (self.com_points-unit.maint) < 0:
                print('------')
                print('Maintenance could not be payed for Player',self.player_num,unit.name)
                print(unit.name,': Destroyed!')
                print('------')
                unit.destroy()
                continue
            print('------')
            self.com_points -= unit.maint
            print('Player',self.player_num,'Paid Maintenance for',unit.name,', Paid',unit.maint)
            print('New Total',self.com_points)
            print('------')
        print('--------------')

    def destroy_unit(self,unit):
        if unit in self.units:
            self.units.remove(unit)
            self.unit_count -= 1

    def get_colony_count(self):
        self.colonies.append(0)
        self.colony_count += 1
        self.col_counter += 1
        return self.colony_count - 1
            
    def create_colony(self, coords, planet, space):
        colonies = self.get_colony_count()
        self.colonies[colonies] = Colony(coords, self, 'Colony',self.colony_count)
        planet.colonized = True
        planet.player = self
        planet.colony = self.colonies[self.colony_count - 1]
        space.colony = self.colonies[self.colony_count - 1]
        print('Player',self.player_num,'Colonized A Planet')

    def build_base(self, coords, colony):
        self.base_count += 0
        colony.base = Base(coords, self, 'Base', self.base_count, colony)
        self.com_points -= 12

    def destroy_colony(self, colony, planet, board_space):
        if colony in self.colonies:
            self.colonies.remove(colony)
            self.colony_count -= 1
        board_space.colony = None
        planet.colonized = False
        planet.player = None
        planet.colony = None
        
            
    def buy_shipyard(self, coords, colony):
        self.shipyard_count += 1
        colony.shipyards.append(0)
        colony.shipyard_count += 1
        colony.shipyards[colony.shipyard_count - 1] = Shipyard(coords, self, 'Shipyard',self.shipyard_count, colony)
        colony.shipyards[colony.shipyard_count - 1].build_capacity = self.tech_lvls[3]
        build = sum([shipyard.build_capacity for shipyard in colony.shipyards])
        colony.builders = build
        
    def destroy_shipyard(self, shipyard, colony):
        if shipyard in colony.shipyards:
            colony.shipyard_count -= 1
            colony.shipyards.remove(shipyard)
            
    def upgrade_shipyards(self):
        for colony in self.colonies:
            for shipyard in colony.shipyards:
                shipyard.build_capacity = self.tech_lvls[3]
            build = sum([shipyard.build_capacity for shipyard in colony.shipyards])
            colony.builders = build

    # def create_unit(self, )

    def initialize_units(self, coords):
        self.coordins = coords
        for r in range(3):
            self.unit_count += 1
            self.unit_counter += 1
            self.units.append(0)
            self.units[self.unit_count - 1] = Scout(coords, self, 'Scout',self.unit_counter)
            self.units[self.unit_count - 1].maint = sum(self.tech_lvls)
        for r in range(3):
            self.unit_count += 1
            self.unit_counter += 1
            self.units.append(0)
            self.units[self.unit_count - 1] = Colonyship(coords, self, 'Colony Ship',self.unit_counter)
            self.units[self.unit_count - 1].maint = sum(self.tech_lvls)
        self.com_points = 0
        self.colonies.append(0)
        self.colony_count += 1
        self.colonies[self.colony_count - 1] = Colony(coords, self, 'Colony',self.colony_count, colony_type = 'Home')
        for i in range(4):
            self.buy_shipyard(coords, self.colonies[self.colony_count - 1])


    def show_unit_coords(self):
        for unit in self.units:
            print(unit.name,':',unit.coords)

