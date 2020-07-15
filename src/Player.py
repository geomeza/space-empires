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
        self.unit_names = []
        self.com_points = com_points
        self.player_num = player_num
        self.coordins = None
        self.colonies = [] 
        self.colony_count = 0
        self.col_counter = 0
        self.shipyards = []
        self.shipyard_count = 0
        self.shipyard_counter = 0

    def add_com_points(self):
        self.com_points += 10

    def generate_cp(self):
        for colony in self.colonies:
            self.com_points += colony.capacity

    def pay_maintenance(self):
        for unit in self.units:
            if (self.com_points-unit.maint) < 0:
                print('Maintenance could not be payed')
                print(unit.name,': Destroyed!')
                unit.destroy()
                continue
            self.com_points -= unit.maint

    def destroy_unit(self,unit):
        if unit in self.units:
            self.units.remove(unit)
            self.unit_count -= 1
            
    def create_colony(self, coords, planet):
        self.colonies.append(0)
        self.colony_count += 1
        self.col_counter += 1
        self.colonies[self.colony_count - 1] = Colony(coords, self, 'Colony',self.colony_count)
        planet.colony = self.colonies[self.colony_count - 1]
        print('Planet Colonized')
        
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
        print(len(colony.shipyards),colony.shipyard_count)
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

    def generate_units(self, coords, colony, only_once = False):
        all_units = [Scout,Destroyer,Cruiser,Battlecruiser,Battleship,Dreadnaught]
        if len(colony.shipyards) == 0:
            self.buy_shipyard(coords, colony)
            print('Bought Shipyard')
            return
        else:
            possible_units = [unit for unit in all_units if unit.hull_size <= colony.builders]
        self.coordins = coords
        while self.com_points >= 6:
            affordable_units = [unit for unit in possible_units if self.com_points >= unit.cost]
            unit_choice = random.randint(0,len(possible_units) - 1)
            while possible_units[unit_choice] not in affordable_units:
                unit_choice = random.randint(0,len(possible_units) - 1)
            self.unit_count += 1
            self.unit_counter += 1
            self.units.append(0)
            self.units[self.unit_count - 1] = possible_units[unit_choice](coords, self, possible_units[unit_choice].name,self.unit_counter)
            if self.units[self.unit_count - 1].name != 'Colony Ship':
                self.units[self.unit_count - 1].strength += self.tech_lvls[0]
                self.units[self.unit_count - 1].defense += self.tech_lvls[1]
                self.units[self.unit_count - 1].speed += self.tech_lvls[2]
            self.units[self.unit_count - 1].maint = self.units[self.unit_count - 1].hull_size
            self.com_points -= possible_units[unit_choice].cost
            if only_once == True:
                break

    def start_units(self, coords):
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
        self.com_points = 20
        self.colonies.append(0)
        self.colony_count += 1
        self.colonies[self.colony_count - 1] = Colony(coords, self, 'Colony',self.colony_count)
        for i in range(4):
            self.buy_shipyard(coords, self.colonies[self.colony_count - 1])

        
    def move_units(self,grid_size):
        for unit in self.units:
            for n in range(unit.speed):
                unit.move(grid_size)

    def show_unit_coords(self):
        for unit in self.units:
            print(unit.name,':',unit.coords)

    def buy_tech(self, tech_num):
        tech = tech_num - 1
        upgraded = 0
        if tech_num == 1 or tech_num == 2:
            if self.com_points < 20:
                print('Not enough combat points')
                return
            if self.com_points >= 20 and self.tech_lvls[tech] == 0 and upgraded == 0:
                self.tech_lvls[tech] += 1
                self.com_points -= 20
                upgraded = 1
            if self.com_points >= 50 and self.tech_lvls[tech] == 1 and upgraded == 0:
                self.tech_lvls[tech] += 1
                self.com_points -= 50
                upgraded = 1
            if self.com_points >= 90 and self.tech_lvls[tech] == 2 and upgraded == 0:
                self.tech_lvls[tech] += 1 
                self.com_points -= 90
                upgraded = 1
            if self.tech_lvls[tech] == 3:
                print('Technology maxed out!')
                return
            if tech_num == 1:
                print('Attack Upgraded')
            if tech_num == 2:
                print('Defense Upgraded')
        if tech_num == 3:
            if self.com_points < 90:
                print('Not enough combat points')
                return
            if self.com_points >= 90 and self.tech_lvls[tech] == 0:
                self.tech_lvls[tech] += 1
                self.com_points -= 90
            if self.com_points >= 210 and self.tech_lvls[tech] == 1:
                self.tech_lvls[tech] += 1
                self.com_points -= 210
            if self.tech_lvls[tech] == 2:
                print('Technology maxed out!')
                return
            print('Speed Upgraded')
        if tech_num == 4:
            
            if self.com_points < 20:
                print('Not enough combat points')
                return
            if self.com_points >= 20 and self.tech_lvls[tech] == 1:
                self.tech_lvls[tech] = 1.5
                self.com_points -= 20
            if self.com_points >= 50 and self.tech_lvls[tech] == 1.5:
                self.tech_lvls[tech] = 2
                self.com_points -= 50
            if self.tech_lvls[tech] == 2:
                print('Technology maxed out!')
                return
            self.upgrade_shipyards()
            print('Shipyard Technology Upgraded')
