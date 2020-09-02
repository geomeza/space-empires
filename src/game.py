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
from players.dumb_player import DumbPlayer
from players.random_player import RandomPlayer
from players.combat_player import CombatPlayer
from combat_engine import CombatEngine
from board import Board
import random
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator   
import sys,os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__



class Game:
    def __init__(self, players=2, player_coords=[[0, 2], [4, 2]], grid_size=[5,5], max_turns=100, planets=8,player_type = 'Random',logging = True, die_rolls = None):
        self.turn_count = 0
        self.player_count = players
        self.turns = 0
        self.win = 0
        self.player_coords = player_coords
        self.grid_size = grid_size
        self.players_dead = 0
        self.max_turns = max_turns
        self.num_planets = planets
        self.board = None
        self.player_type = player_type
        self.combat_engine = None
        self.complete = False
        self.die_rolls = die_rolls
        if logging is False:
            blockPrint()

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
        self.combat_engine = CombatEngine(self.board, dice_type = self.die_rolls)

    def update_board(self):
        all_units = []
        for player in self.players:
            for unit in player.units:
                all_units.append(unit)
        self.board.update_self(all_units)

    def generate_players(self):
        if self.player_type == 'Random':
            self.players = [RandomPlayer(i + 1) for i in range(self.player_count)]
        
        if self.player_type == 'Dumb':
            self.players = [DumbPlayer(i + 1) for i in range(self.player_count)]
        
        if self.player_type == 'Combat':
            self.players = [CombatPlayer(i + 1, self.grid_size) for i in range(self.player_count)]

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

    def upgrade(self,player):
        upgr = random.randint(1, 2)
        if upgr == 1:
            player.buy_tech()
        elif upgr == 2:
            colony_choice = random.choice(player.colonies)
            player.generate_units(colony_choice.coords, colony_choice, only_once =True)

    def colonize(self, player):
        for unit in player.units:
            space = self.board.grid[tuple(unit.coords)]
            if unit.name == 'Colony Ship':
                if space.planet is not None:
                    if space.planet.colonized is False:
                        space.planet.player = player
                        space.planet.colonized = True
                        unit.destroy()
                        player.create_colony(unit.coords, space.planet, space)

    def start(self):
        self.create_board()
        self.generate_players()
        self.update_board()
        for s in range(len(self.players)):
            print('----------------------------------')
            print('Player', s + 1, ':')
            print('Combat Points:',self.players[s].com_points)
            self.show_unit_coords(s+1)
            print('----------------------------------')

    def complete_movement_phase(self):
        print('BEGINNING OF MOVEMENT PHASE')
        print('-----------------------------------------')
        self.complete_first_movement()
        self.complete_second_movement()
        self.complete_third_movement()
        print('-----------------------------------------')
        print('END OF MOVEMENT PHASE')

    def complete_first_movement(self):
        movements = 0
        print('--------------------------------------')
        print('FIRST MOVEMENT')
        for player in self.players:
            if player.tech_lvls[2] <= 3:
                movements = 1
            else:
                movements = 2
            print('--------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.grid_size, movements)
            print('--------------------------------')
        print('--------------------------------------')

    def complete_second_movement(self):
        movements = 0
        print('--------------------------------------')
        print('SECOND MOVEMENT')
        for player in self.players:
            if player.tech_lvls[2] <= 1:
                movements = 1
            elif player.tech_lvls[2] <= 5:
                movements = 2
            else:
                movements = 3
            print('--------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.grid_size, movements)
            print('--------------------------------')
        print('--------------------------------------')

    def complete_third_movement(self):
        movements = 0
        print('--------------------------------------')
        print('THIRD MOVEMENT')
        for player in self.players:
            if player.tech_lvls[2] <= 1:
                movements = 1
            elif player.tech_lvls[2] <= 4:
                movements = 2
            else:
                movements = 3
            print('--------------------------------')
            print('Player',player.player_num,'is moving')
            player.move_units(self.grid_size, movements)
            print('--------------------------------')
        print('--------------------------------------')

    def complete_combat_phase(self):
        print('----------------------------------')
        print('BEGINNING OF COMBAT PHASE')
        self.resolve_combat()
        for player in self.players:
            self.combat_engine.attack_colony(player)
        print('END OF COMBAT PHASE')
        print('----------------------------------')

    def complete_economic_phase(self):
        print('----------------------------------')
        print('BEGINNING OF ECONOMIC PHASE')
        self.add_combat_points()
        self.pay_maintenance_cost()
        for player in self.players:
            self.colonize(player)
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
        self.remove_dead_players()
        if self.complete is True:
            self.winner()
            return None
        self.complete_economic_phase()
        self.remove_dead_players()
        if self.complete is True:
            self.winner()
            return None
        print('-------------------------------------')
        print('PLAYERS LEFT:')
        for player in self.players:
            print('PLAYER',player.player_num)
        self.turns +=1
        print('-------------------------------------------------')
        return None

    def remove_dead_players(self):
        for player in self.players:
            if len(player.units) == 0 and len(player.colonies) == 0:
                print('-------------------------------------------')
                print('PLAYER',player.player_num,'HAD NO MORE SHIPS')
                print('PLAYER',player.player_num,'DIED')
                self.players_dead += 1
                self.players.remove(player)
                print('-------------------------------------------')
        if len(self.players) == 1:
            self.win = self.players[0].player_num
            self.complete = True
            return None

    def complete_many_turns(self,nums):
        for n in range(nums):
            if self.complete is False:
                self.complete_turn()

    def resolve_combat(self):
        all_units = []
        for player in self.players:
            for unit in player.units:
                all_units.append(unit)
        occupants = self.board.occupy(all_units)
        for o in occupants:
            if len(o) >= 2:
                self.combat_engine.check_for_battle(o)
    
    def state(self):
        for player in self.players:
            print('Player:',player.player_num)
            for unit in player.units:
                unit.show_coords()

    def run_to_completion(self):
        for n in range(self.turns, self.max_turns):
            if self.complete is False:
                self.complete_turn()
            else:
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