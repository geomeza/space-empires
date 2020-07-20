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
from Players.Player import Player
import random

class dumb_player(Player):       

    def generate_units(self, coords, colony, only_once = False):
        if only_once is True:
            only_once = False
        all_units = [Scout]
        possible_units = [unit for unit in all_units if unit.hull_size <= colony.builders]
        self.coordins = coords
        if self.com_points <6:
            print('Couldnt afford any units')
        while self.com_points >= 6:
            affordable_units = [unit for unit in possible_units if self.com_points >= unit.cost]
            unit_choice = random.randint(0,len(possible_units) - 1)
            while possible_units[unit_choice] not in affordable_units:
                unit_choice = random.randint(0,len(possible_units) - 1)
            self.unit_count += 1
            self.unit_counter += 1
            self.units.append(0)
            print('Bought:',possible_units[unit_choice].name)
            self.units[self.unit_count - 1] = possible_units[unit_choice](coords, self, possible_units[unit_choice].name,self.unit_counter)
            if self.units[self.unit_count - 1].name != 'Colony Ship':
                self.units[self.unit_count - 1].strength += self.tech_lvls[0]
                self.units[self.unit_count - 1].defense += self.tech_lvls[1]
                self.units[self.unit_count - 1].speed += self.tech_lvls[2]
            self.units[self.unit_count - 1].maint = self.units[self.unit_count - 1].hull_size
            self.com_points -= possible_units[unit_choice].cost
            if only_once == True:
                break

        
    def move_units(self,grid_size):
        for unit in self.units:
            before_coords = unit.coords
            if unit.name == 'Scout':
                for n in range(unit.speed):
                    unit.move(grid_size, only_direction = [-1,0])
                print(unit.name,':',before_coords,'-->',unit.coords)

    def buy_tech(self):
        self.generate_units(self.coordins,self.colonies[0],only_once = True)
