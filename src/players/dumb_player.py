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
from planets.planet import Planet
from players.player import Player
import random

class DumbPlayer(Player):  

    def __init__(self, player_num):
        super().__init__(player_num)
        self.player_type = 'Dumb'     

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

        
    def move_units(self,grid_size, range_of_movements):
        for unit in self.units:
            before_coords = unit.coords
            if unit.name == 'Scout':
                for n in range(range_of_movements):
                    unit.move(grid_size, only_direction = [-1,0])
                print(unit.name,':',before_coords,'-->',unit.coords)

    def buy_tech(self):
        self.generate_units(self.coordins,self.colonies[0],only_once = True)

    def unit_preference(self, units):
        return random.choice(units)
