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

class CombatPlayer(Player):

    def __init__(self, player_num, grid_size):
        super().__init__(player_num)
        self.player_type = 'Combat'
        self.buy_count = 0
        self.grid_size = grid_size

    def move_units(self,grid_size, range_of_movements):
        for unit in self.units:
            before_coords = unit.coords   
            for n in range(range_of_movements):
                unit.move(grid_size)
            print(unit.name,':',before_coords,'-->',unit.coords)

    def initialize_units(self, coords):
        super().initialize_units(coords)
        for unit in self.units:
            unit.set_route([self.grid_size[0]//2, self.grid_size[1]//2])

    def generate_units(self, coords, colony, only_once = False):
        if only_once is True:
            only_once = False
        if self.tech_lvls[3] < 1.5:
            self.buy_tech()
            return None
        if self.buy_count % 2 == 0:
            all_units = [Destroyer]
        else:
            all_units = [Scout]
        possible_units = [unit for unit in all_units if unit.hull_size <= colony.builders]
        self.coordins = coords
        if self.com_points < 6 or len(possible_units) == 0:
            print('Couldnt afford to buy any units')
            return None
        while self.com_points >= 6:
            affordable_units = all_units
            unit_choice = 0
            if all_units[0].cost > self.com_points:
                print('Couldnt afford any units')
                return None
            self.unit_count += 1
            self.unit_counter += 1
            self.units.append(0)
            print('Bought:',possible_units[unit_choice].name)
            self.units[self.unit_count - 1] = possible_units[unit_choice](coords, self, possible_units[unit_choice].name,self.unit_counter)
            self.buy_count += 1
            if self.units[self.unit_count - 1].name != 'Colony Ship':
                self.units[self.unit_count - 1].strength += self.tech_lvls[0]
                self.units[self.unit_count - 1].defense += self.tech_lvls[1]
                self.units[self.unit_count - 1].speed += self.tech_lvls[2]
            self.units[self.unit_count - 1].maint = self.units[self.unit_count - 1].hull_size
            self.units[self.unit_count - 1].set_route([self.grid_size[0]//2, self.grid_size[1]//2])
            self.com_points -= possible_units[unit_choice].cost
            if only_once == True:
                break 

    def buy_tech(self):
        tech_num = 4
        tech = tech_num - 1
        upgraded = 0
        if self.tech_lvls[tech] == 2:
            colony = random.choice(self.colonies)
            self.generate_units(colony.coords, colony)
            return None
        if tech_num == 4:    
            if self.com_points < 20:
                print('Not enough combat points')
                return
            if self.com_points >= 20 and self.tech_lvls[tech] == 1 and upgraded == 0:
                self.tech_lvls[tech] = 1.5
                self.upgrade_shipyards()
                self.com_points -= 20
                upgraded = 1
            if self.com_points >= 50 and self.tech_lvls[tech] == 1.5 and upgraded == 0:
                self.tech_lvls[tech] = 2
                self.upgrade_shipyards()
                self.com_points -= 50
                upgraded = 1
            print('Shipyard Technology Upgraded')

    def unit_preference(self, units):
        return units[-1]