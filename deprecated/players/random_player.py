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

class RandomPlayer(Player):

    def __init__(self, player_num):
        super().__init__(player_num)
        self.player_type = 'Random'

    def move_units(self, grid_size, range_of_movements):
        for unit in self.units:
            before_coords = unit.coords
            for n in range(range_of_movements):
                unit.move(grid_size)
            print(unit.name,':',before_coords,'-->',unit.coords)

    def buy_tech(self):
        tech_num = random.randint(1,4)
        tech = tech_num - 1
        upgraded = 0
        if tech_num == 1 or tech_num == 2:
            tech_lvl = self.tech_lvls[tech]
            cost = [20, 50, 90]
            if self.com_points < cost[tech_lvl]:
                print('Could not afford attack/defense')
                return
            if tech_lvl == len(cost):
                if tech_num == 1:
                    print('Attack Maxed Out!')
                else:
                    print('Defense Maxed Out!')
                return None
            if self.com_points >= cost[tech_lvl]:
                self.tech_lvls[tech] += 1
                self.com_points -= cost[tech_lvl]
            if tech_num == 1:
                print('Attack Upgraded')
            if tech_num == 2:
                print('Defense Upgraded')
        if tech_num == 3:
            tech_lvl = self.tech_lvls[tech] - 1
            cost = [20, 50, 90, 130, 170]
            if self.com_points < cost[tech_lvl]:
                print('Could not afford movement technology')
                return
            if tech_lvl == len(cost):
                print('Movement Technology Maxed Out')
                return None
            if self.com_points >= cost[tech_lvl]:
                self.tech_lvls[tech] += 1
                self.com_points -= cost[tech_lvl]
            print('Movement Technology Upgraded')
            return None
        if tech_num == 4: 
            cost = [20, 50]
            if self.tech_lvls[tech] == 1.5:
                tech_lvl = 1
            elif self.tech_lvls[tech] == 2.0:
                tech_lvl = 2
            else:
                tech_lvl = 0
            if self.com_points < cost[tech_lvl]:
                print('Could not upgrade  shipyards')
                return
            if self.tech_lvls[tech] == 2:
                print('Shipyard technology maxed out!')
                return
            if self.com_points >= cost[tech_lvl]:
                self.tech_lvls[tech] += 0.5
                self.upgrade_shipyards()
                self.com_points -= cost[tech_lvl]
            print('Shipyard Technology Upgraded')

    
    def generate_units(self, coords, colony, only_once = False):
        choicer = random.randint(1,2)
        all_units = [Scout,Colonyship,Destroyer,Cruiser,Battlecruiser,Battleship,Dreadnaught]
        if colony.base is None:
            if self.com_points >= 12:
                self.build_base(coords, colony)
                print('Built Base On Colony at', coords)
            else:
                print('Could not buy Base')
            return
        if len(colony.shipyards) == 0:
            if self.com_points >= 6:
                self.buy_shipyard(coords, colony)
                self.com_points -= 6
                print('Bought Shipyard')
            else:
                print('Could not buy shipyard')
            return
        elif choicer == 1:
            if self.com_points >= 6:
                self.buy_shipyard(coords, colony)
                self.com_points -= 6
                print('Bought Shipyard')
            else:
                print('Could not buy shipyard')
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

    def unit_preference(self, units):
        return random.choice(units)

    def will_colonize(self):
        return True

    def upgrade(self):
        num = random.int(1,2)
        if num == 1:
            self.buy_tech()
        elif num == 2:
            colony_choice = random.choice(self.colonies)
            self.generate_units(colony_choice.coords, colony_choice, only_once =True)