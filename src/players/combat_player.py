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

    def sort(self):
        for i in range(len(self.units)):
            for j in range(i + 1, len(self.units)):
                unit1 = self.units[i]
                unit2 = self.units[j]
                u1_tactics = unit1.player.tech_lvls[0] + unit1.player.tech_lvls[1]
                u2_tactics = unit2.player.tech_lvls[0] + unit2.player.tech_lvls[1]
                if (unit1.class_num + u1_tactics) < (unit2.class_num + u2_tactics):
                    self.units[i], self.units[j] = self.units[j], self.units[i]
        return self.units

    def pay_maintenance(self):
        self.sort()
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
        if self.tech_lvls[4] < 2:
            self.buy_tech()
            return None
        if self.buy_count % 2 == 0:
            all_units = [Destroyer]
        else:
            all_units = [Scout]
        possible_units = [unit for unit in all_units if unit.hull_size <= colony.builders and self.tech_lvls[4] >= unit.hull_size]
        self.coordins = coords
        if self.com_points < 6 or len(possible_units) == 0:
            print('Couldnt afford to buy any units')
            return None
        while self.com_points >= 6:
            if self.buy_count % 2 == 0:
                all_units = [Destroyer]
            else:
                all_units = [Scout]
            possible_units = [unit for unit in all_units if unit.hull_size <= colony.builders and self.tech_lvls[4] >= unit.hull_size]
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
        tech_num = 5
        tech = tech_num - 1
        upgraded = 0
        if tech_num == 5 and self.tech_lvls[tech] != 2:
            tech_lvl = self.tech_lvls[tech] - 1
            cost = [10, 25, 45, 70, 100]
            if tech_lvl == 5:
                print('Ship Size technology Maxed Out')    
            if self.com_points < cost[tech_lvl]:
                print('Not enough combat points')
                return
            if self.com_points >= cost[tech_lvl]:
                self.tech_lvls[tech] += 1
                self.com_points -= cost[tech_lvl]
            print('Ship Size Technology Upgraded')
        if self.tech_lvls[tech] == 2:
            colony = random.choice(self.colonies)
            self.generate_units(colony.coords, colony)
            return None

    def unit_preference(self, units):
        return units[0]