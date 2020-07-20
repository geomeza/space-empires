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
from Players.dumb_player import dumb_player
from board import Board
import random
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator            


class Game():
    def __init__(self, players=2, player_coords=[[0, 2], [4, 2]], combat_points=50, grid_size=[5,5], max_turns=100, planets=8,dumb_players = False):
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
        self.board = None
        self.dumb_players = dumb_players

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

    def create_board(self):
        self.board = Board(self.grid_size)
        self.board.generate()
        self.board.generate_planets(self.player_coords, self.num_planets)

    def update_board(self):
        all_units = []
        for player in self.players:
            for unit in player.units:
                all_units.append(unit)
        self.board.update_self(all_units)

    def generate_players(self):
        if self.dumb_players is False:
            self.players = [Player(self.combat_points,i + 1) for i in range(self.player_count)]
        if self.dumb_players is True:
            self.players = [dumb_player(self.combat_points,i + 1) for i in range(self.player_count)]
        for s in range(self.player_count):
            self.players[s].initialize_units(self.player_coords[s])

    def add_combat_points(self):
        for player in self.players:
            player.generate_cp()

    def pay_maintenance_cost(self):
        for player in self.players:
            player.pay_maintenance()

    def show_unit_coords(self, player_num):
        for unit in self.players[player_num - 1].units:
            print(unit.name, ':', unit.coords)

    def colonize(self, player):
        for unit in player.units:
            space = self.board.grid[tuple(unit.coords)]
            ##### CHANGE THIS WITH BOARD, I THINK ITS CHANGED
            if unit.name == 'Colony Ship':
                if space.planet is not None:
                    if space.planet.colonized is False:
                        space.planet.player = player
                        space.planet.colonized = True
                        unit.destroy()
                        player.create_colony(unit.coords, space.planet, space)
            else:
                if space.planet is not None:
                    if space.planet.player != player:
                        if space.planet.colonized is True:
                            if len(space.planet.colony.shipyards) > 0:
                                shipy_choice = random.choice(space.planet.colony.shipyards)
                                self.battle(unit, shipy_choice)
                            else:
                                print('----------------------------------')
                                print('Player',unit.player.player_num,'Encountered a Colony')
                                self.colony_shot(unit, space.planet.colony)



    def upgrade(self,player):
        upgr = random.randint(1, 2)
        if upgr == 1:
            player.buy_tech()
        elif upgr == 2:
            colony_choice = random.choice(player.colonies)
            player.generate_units(colony_choice.coords, colony_choice, only_once =True)

    def start(self):
        self.generate_players()
        self.create_board()
        self.update_board()
        for s in range(len(self.players)):
            print('----------------------------------')
            print('Player', s + 1, ':')
            print('Combat Points:',self.players[s].com_points)
            self.show_unit_coords(s+1)
            print('----------------------------------')

    def complete_movement_phase(self):
        print('BEGINNING OF MOVEMENT PHASE')
        for player in self.players:
            print('----------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.grid_size)
            print('----------------------------------')
        print('END OF MOVEMENT PHASE')

    def complete_combat_phase(self):
        print('----------------------------------')
        print('BEGINNING OF COMBAT PHASE')
        self.resolve_combat()
        for player in self.players:
            self.colonize(player)
        print('END OF COMBAT PHASE')
        print('----------------------------------')

    def complete_economic_phase(self):
        print('----------------------------------')
        print('BEGINNING OF ECONOMIC PHASE')
        self.add_combat_points()
        self.pay_maintenance_cost()
        for player in self.players:
            print('-----------')
            print('Player',player.player_num,'is upgrading/buying!')
            self.upgrade(player)
            print('Player',player.player_num,'Combat Points Left:',player.com_points)
            print('-----------')
        print('END OF ECONOMIC PHASE')
        print('----------------------------------')


    def complete_turn(self):
        print('-------------------------------------------------')
        print('Turn', self.turns + 1)
        self.complete_movement_phase()
        self.complete_combat_phase()
        self.complete_economic_phase()
        self.check_death()
        self.turns +=1
        print('-------------------------------------------------')
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
                        print('----------------------------------')
                        print('Combat at:', unit1.coords)
                        print('Player',unit1.player.player_num, ',', unit1.name)
                        print('VS')
                        print('Player', unit2.player.player_num, ',', unit2.name)
                        battler = self.battle(unit1,unit2)
                        print('----------------------------------')

    def colony_shot(self, unit1, colony):
        threshold = unit1.strength - 3
        dice_roll = random.randint(0,6)
        if dice_roll > threshold:
            if colony.capacity > 1:
                print('Colony Hit!')
                colony.capacity -= 1
            else:
                print('Colony Destroyed')
                self.board.grid[tuple(colony.coords)].planet.colonized = False
                self.board.grid[tuple(colony.coords)].planet.player = None
                self.board.grid[tuple(colony.coords)].planet.colony = None
                self.board.grid[tuple(colony.coords)].colony = None
                colony.player.destroy_colony(colony)
        else:
            print('Colony Missed')

    def battle(self, unit1, unit2):### CHANGE THIS FUNCTION
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
                    print('------')
                    print('Player',fight_order[0].player.player_num, fight_order[0].name,'Was Hit!')
                    fight_order[0].armor -= 1
                    print('------')
                else:
                    print('------')
                    print('Player',fight_order[0].player.player_num, fight_order[0].name,' Was Destroyed!')
                    print('Survivor: Player', fight_order[1].player.player_num, ',',fight_order[1].name)
                    fight_order[0].destroy()
                    return fight_order[1]
            else:
                print('------')
                print('Player',fight_order[0].player.player_num, fight_order[0].name,' Was Missed!')
                print('------')
            fight_order.reverse()
                                     
    def hit_threshold(self, unit1, unit2):
        return unit1.strength - unit2.defense

    def class_supremacy(self, unit1, unit2):
        ## CHANGE BELOW LOL
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

    #### CHANGE ABOVE LOL
    
    def state(self):
        for player in self.players:
            print('Player:',player.player_num)
            for unit in player.units:
                unit.show_coords()

    def run_to_completion(self):
        for n in range(self.turns, self.max_turns):
            self.complete_turn()
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