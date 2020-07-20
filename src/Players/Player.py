from Units.Unit import Unit 
from Units.Dreadnaught import Dreadnaught 
from Units.Scout import Scout 
from Units.Battlecruiser import Battlecruiser 
from Units.Battleship import Battleship 
from Units.Colony import Colony 
from Units.Colonyship import Colonyship 
from Units.Cruiser import Cruiser 
from Units.Destroyer import Destroyer 
from Units.Shipyard import Shipyard 
from Planets.Planet import Planet 
import random

class Player():
    def __init__(self, com_points,player_num):
        self.tech_lvls = [0, 0, 0, 1]
        self.unit_count = 0
        self.unit_counter = 0
        self.units = []
        self.com_points = com_points
        self.player_num = player_num
        self.coordins = None
        self.colonies = [] 
        self.colony_count = 0
        self.col_counter = 0
        self.shipyards = []
        self.shipyard_count = 0
        self.shipyard_counter = 0

    def generate_cp(self):
        print('--------------')
        total_cp = 0
        for colony in self.colonies:
            total_cp += colony.capacity
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
                unit.maint = 0
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
            
    def create_colony(self, coords, planet, space):
        self.colonies.append(0)
        self.colony_count += 1
        self.col_counter += 1
        self.colonies[self.colony_count - 1] = Colony(coords, self, 'Colony',self.colony_count)
        planet.player = self
        planet.colony = self.colonies[self.colony_count - 1]
        space.colony = self.colonies[self.colony_count - 1]
        print('Player',self.player_num,'Colonized A Planet')
        
    def destroy_colony(self, colony):
        if colony in self.colonies:
            self.colonies.remove(colony)
            self.colony_count -= 1
            
    def buy_shipyard(self, coords, colony):
        self.shipyards.append(0)
        self.shipyard_count += 1
        self.shipyards[self.shipyard_count - 1] = Shipyard(coords, self, 'Shipyard',self.shipyard_count, colony)
        colony.shipyards.append(0)
        colony.shipyard_count += 1
        colony.shipyards[colony.shipyard_count - 1] = Shipyard(coords, self, 'Shipyard',self.shipyard_count, colony)
        colony.builders = sum([shipyard.build_capacity for shipyard in colony.shipyards])
        
    def destroy_shipyard(self, shipyard, colony):
        if shipyard in colony.shipyards:
            colony.shipyard_count -= 1
            colony.shipyards.remove(shipyard)
            
    def upgrade_shipyards(self):
        for shipyard in self.shipyards:
            shipyard.build_capacity = self.tech_lvls[3]
        for colony in self.colonies:
            colony.builders = sum([shipyard.build_capacity for shipyard in colony.shipyards])

    def initialize_units(self, coords):
        self.coordins = coords
        for r in range(3):
            self.unit_count += 1
            self.unit_counter += 1
            self.units.append(0)
            self.units[self.unit_count - 1] = Scout(coords, self, 'Scout',self.unit_counter)
            self.units[self.unit_count - 1].maint = sum(self.tech_lvls)
        # for r in range(8):
        #     self.unit_count += 1
        #     self.unit_counter += 1
        #     self.units.append(0)
        #     self.units[self.unit_count - 1] = Colonyship(coords, self, 'Colony Ship',self.unit_counter)
        #     self.units[self.unit_count - 1].maint = sum(self.tech_lvls)
        self.com_points = 20
        self.colonies.append(0)
        self.colony_count += 1
        self.colonies[self.colony_count - 1] = Colony(coords, self, 'Colony',self.colony_count)
        for i in range(4):
            self.buy_shipyard(coords, self.colonies[self.colony_count - 1])

    def show_unit_coords(self):
        for unit in self.units:
            print(unit.name,':',unit.coords)

