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
from Player import Player 
import random
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator            


class Game():
    def __init__(self, players=2, player_coords=[[0, 2], [4, 2]], combat_points=50, grid_size=[5,5], max_turns=100, planets=8):
        self.turn_count = 0
        self.current_player = 0
        self.player_count = players
        self.turns = 0
        self.win = 0
        self.player_coords = player_coords
        self.combat_points = combat_points
        self.grid_size = grid_size
        self.players_dead = 0
        self.max_turns = max_turns
        self.num_planets = planets
        self.planets = []
        self.planet_coords = []

    # def labeled_scatter_plot(self, grid_size=[5,5], fontsize=10):
    #     player_colors = ['red','blue','green','purple']
    #     fig, ax = plt.subplots()
    #     ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    #     ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    #     for i in range(len(self.players)):
    #         for unit in self.players[i].units:
    #             team_color = player_colors[self.players[i].player_num - 1]
    #             x = unit.coords[0]
    #             y = unit.coords[1]
    #             color = team_color
    #             label = unit.abbr+str(unit.unit_num)
    #             ax.text(x, y, label, fontsize=fontsize, color=color, horizontalalignment='center', verticalalignment='center')
    #     for planet in self.planets:
    #         p_coords = planet.coords
    #         ax.text(p_coords[0], p_coords[1], 'Planet', fontsize=10, color='black', horizontalalignment='center', verticalalignment='center')
    #     x_max, y_max = grid_size
    #     plt.xlim(-0.5 ,x_max-0.5)
    #     plt.ylim(-0.5, y_max-0.5)

    #     plt.grid(which='minor')
    #     plt.show()

    def generate_players(self):
        self.players = [Player(self.combat_points,i + 1) for i in range(self.player_count)]
        for s in range(self.player_count):
            # print(self.players[s])
            # print(s,self.player_coords[s])
            self.players[s].start_units(self.player_coords[s])

    def generate_coordinates(self):
        x_coord = random.randint(0,self.grid_size[0] - 1)
        y_coord = random.randint(0,self.grid_size[1] - 1)
        return [x_coord,y_coord]

    def generate_planets(self):
        self.planet_coords = []
        for k in range(self.num_planets):
            coords = self.generate_coordinates()
            while coords in self.player_coords and coords in self.planet_coords:
                coords = self.generate_coordinates()
            self.planet_coords.append(coords)
            self.planets.append(0)
            self.planets[k] = Planet(coords)
                    

    def add_combat_points(self):
        for player in self.players:
            player.generate_cp()

    def maint_cost(self):
        for player in self.players:
            player.pay_maintenance()

    def show_unit_coords(self, player_num):
        for unit in self.players[player_num - 1].units:
            print(unit.name, ':', unit.coords)

    def move_units(self, player_num):
        for unit in self.players[self.current_player].units:
            before_coords = unit.coords
            for n in range(unit.speed):
                unit.move(self.grid_size)
            print(unit.name,':',before_coords,'-->',unit.coords)

    def colonize(self, player_num):
        player = self.players[player_num - 1]
        for unit in player.units:
            if unit.name == 'Colony Ship':
                if unit.coords in self.planet_coords:
                    planet_index = self.planet_coords.index(unit.coords)
                    planet = self.planets[planet_index]
                    if planet.colonized is False:
                        planet.player = player
                        planet.colonized = True
                        unit.destroy()
                        player.create_colony(unit.coords, planet)
            else:
                if unit.coords in self.planet_coords:
                    planet_index = self.planet_coords.index(unit.coords)
                    planet = self.planets[planet_index]
                    if planet.colonized is True:
                        if len(planet.colony.shipyards) > 0:
                            shipy_choice = random.choice(planet.colony.shipyards)
                            print(shipy_choice.defense,unit.strength)
                            self.battle(unit, shipy_choice)
                        else:
                            self.colony_shot(unit, planet.colony)



    def upgrade(self,player_num):
        num = player_num - 1
        upgr = random.randint(1, 5)
        if upgr <= 4:
            self.players[num].buy_tech(upgr)
        elif upgr == 5:
            colony_choice = random.choice(self.players[num].colonies)
            self.players[num].generate_units(colony_choice.coords, colony_choice, only_once =True)

    def start(self):
        self.generate_planets()
        self.generate_players()
        for s in range(len(self.players)):
            print('----------------------------------')
            print('Player', s + 1, ':')
            self.show_unit_coords(s+1)
            print('----------------------------------')

    def complete_turn(self):
        print('----------------')
        if self.current_player >= len(self.players):
            self.current_player = 0
        current_player = self.players[self.current_player]
        print('Turn', self.turns + 1)
        print('Player',current_player.player_num)
        self.add_combat_points()
        self.maint_cost()
        self.upgrade(self.current_player)
        self.colonize(self.current_player)
        self.move_units(current_player.player_num - 1)
        print('Combat Points Left:',current_player.com_points)
        # self.labeled_scatter_plot(grid_size = self.grid_size)
        self.turns +=1
        self.current_player += 1
        if self.current_player >= len(self.players):
            self.current_player = 0
        print('----------------')
        return None

    def check_death(self):
        for player in self.players:
            if len(player.units) == 0:
                self.players_dead += 1
                self.players.remove(player)

    def complete_many_turns(self,nums):
        for n in range(nums):
            self.complete_turn()

    def resolve_combat(self):
        all_units = []
        for player in self.players:
            for unit in player.units:
                all_units.append(unit)
        for u1_index in range(len(all_units)):
            for u2_index in range(u1_index + 1,len(all_units)):
                unit1 = all_units[u1_index]
                unit2 = all_units[u2_index]
                if unit1.player != unit2.player:
                    if unit1.coords == unit2.coords:
                        print('Combat at:', unit1.coords)
                        print('Player',unit1.player.player_num, ',', unit1.name)
                        print('VS')
                        print('Player', unit2.player.player_num, ',', unit2.name)
                        battler = self.battle(unit1,unit2)
                        # return None

    def colony_shot(self, unit1, colony):
        threshold = unit1.strength - 3
        dice_roll = random.randint(0,6)
        if dice_roll > threshold:
            if colony.capacity > 1:
                print('Colony Hit!')
                colony.capacity -= 1
            else:
                print('Colony Destroyed')
                colony.player.destroy_colony(colony)
        else:
            print('Colony Missed')

    def battle(self, unit1, unit2):
        first = self.class_supremacy(unit1,unit2)
        if first == 1:
            fight_order = [unit1,unit2]
        else:
            fight_order = [unit2,unit1]

        while unit1.alive == True and unit2.alive == True:
            threshold = self.hit_threshold(fight_order[0],fight_order[1]) 
            dice_roll = random.randint(0,6)
            if dice_roll > threshold or dice_roll == 1:
                if fight_order[0].armor > 0:
                    fight_order[0].armor -= 1
                else:
                    print('Hit')
                    print('Survivor: Player', fight_order[1].player.player_num, ',',fight_order[1].name)
                    fight_order[0].destroy()
                    return fight_order[1]
            fight_order.reverse()
                                     
    def hit_threshold(self, unit1, unit2):
        print(unit1.name,unit2.name)
        print(unit1.strength,unit2.defense)
        return unit1.strength - unit2.defense

    def class_supremacy(self, unit1, unit2):
        if unit1.class_num > unit2.class_num:
            return 1
        elif unit2.class_num > unit1.class_num:
            return 2
        elif unit1.class_num == unit2.class_num:
            return random.randint(1,2) 

    def supremacy(self,units):
        for unit in units:
            print('nah')
			

    def new_battle(self,units):
        battle_order = []
        for unit in bruh:
            print('nah')
    
    def state(self):
        for player in self.players:
            print('Player:',player.player_num)
            for unit in player.units:
                unit.show_coords()

    def run_to_completion(self):
        for n in range(self.turns, self.max_turns):
            self.complete_turn()
            self.resolve_combat()
            self.check_death()
            if len(self.players) == 1:
                self.win = self.players[0].player_num
                print('Game Over')
                return None
        self.win = self.player_count + 2
        print('Game Over')

    def winner(self):
        if self.win == 0:
            return ('Game Not Done Yet')
        elif self.win in range(self.player_count + 1):
            print('Player', self.win, 'Wins')
        else:
            return ('Nobody Wins')