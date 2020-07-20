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

class random_player(Player):

    def move_units(self,grid_size):
        for unit in self.units:
            before_coords = unit.coords
            for n in range(unit.speed):
                unit.move(grid_size)
            print(unit.name,':',before_coords,'-->',unit.coords)

    def buy_tech(self):
        tech_num = random.randint(1,4)
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

    def generate_units(self, coords, colony, only_once = False):
        choicer = random.randint(1,2)
        all_units = [Scout,Destroyer,Cruiser,Battlecruiser,Battleship,Dreadnaught,Colonyship]
        if len(colony.shipyards) == 0:
            self.buy_shipyard(coords, colony)
            print('Bought Shipyard')
            return
        elif choicer == 1:
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