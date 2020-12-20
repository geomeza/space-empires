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
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
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
        self.phase = None
        self.current_player = None
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
        self.movement_engine = None
        self.economic_engine = None
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

    def generate_state(self):
        game_dict = {}
        game_attrs = ['turn', 'phase', 'current player', 'winner', 'players']
        game_iterators = ['turns', 'phase', 'current_player', 'win', 'players']
        for attr, val in self.__dict__.items():
            if attr in game_iterators:
                ind_of_iter = game_iterators.index(attr)
                if game_attrs[ind_of_iter] != 'players':
                    game_dict[game_attrs[ind_of_iter]] = val
                else:
                    game_dict['players'] = []
                    for player in self.players:
                        player_dict = self.generate_player_dict(player)
                        game_dict['players'].append(player_dict)
        game_dict['planets'] = [planet.coords for planet in self.board.planets]
        return game_dict

    def generate_player_dict(self, player):
        player_dict = {}
        player_dict['cp'] = player.com_points
        player_tech = ['attack', 'defense', 'movement', 'Ship size']
        player_dict['technology'] = {player_tech[i]: player.tech_lvls[i] for i in range(len(player_tech))}
        units = [self.generate_unit_dict(unit) for unit in player.units]
        for colony in player.colonies:
            units.append(self.generate_unit_dict(colony))
        player_dict['units'] = units
        return player_dict

    def generate_unit_dict(self, unit):
        unit_dict = {}
        unit_dict['location'] = unit.coords
        if unit.name == 'Colony':
            unit_dict['type'] = unit.colony_type
        else:
            unit_dict['type'] = unit.name
            unit_dict['health'] = unit.armor
            unit_dict['technology'] = {}
            unit_dict['technology']['attack'] = unit.strength
            unit_dict['technology']['defense'] = unit.defense
            unit_dict['technology']['movement'] = unit.speed
        return unit_dict

    def create_board(self):
        self.board = Board(self.grid_size)
        self.board.generate()
        self.board.generate_planets(self.player_coords, self.num_planets)
        self.combat_engine = CombatEngine(self.board, dice_type = self.die_rolls)
        self.movement_engine = MovementEngine(self, self.board)

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

    # def add_combat_points(self):
    #     for player in self.players:
    #         player.generate_cp()

    # def pay_maintenance_cost(self):
    #     for player in self.players:
    #         player.pay_maintenance()

    def show_unit_coords(self, player_num):
        for unit in self.players[player_num - 1].units:
            print(unit.name, ':', unit.coords)

    # def upgrade(self,player):
    #     upgr = random.randint(1, 2)
    #     if upgr == 1:
    #         player.buy_tech()
    #     elif upgr == 2:
    #         colony_choice = random.choice(player.colonies)
    #         player.generate_units(colony_choice.coords, colony_choice, only_once =True)

    # def colonize(self, player):
    #     if player.will_colonize():
    #         for unit in player.units:
    #             space = self.board.grid[tuple(unit.coords)]
    #             if unit.name == 'Colony Ship':
    #                 if space.planet is not None:
    #                     if space.planet.colonized is False:
    #                         space.planet.player = player
    #                         space.planet.colonized = True
    #                         unit.destroy()
    #                         player.create_colony(unit.coords, space.planet, space)

    def start(self):
        self.create_board()
        self.generate_players()
        self.economic_engine = EconomicEngine(self.board, self, self.players)
        self.update_board()
        for s in range(len(self.players)):
            print('----------------------------------')
            print('Player', s + 1, ':')
            print('Combat Points:',self.players[s].com_points)
            self.show_unit_coords(s+1)
            print('----------------------------------')

    def complete_combat_phase(self):
        self.phase = 'Combat'
        print('----------------------------------')
        print('BEGINNING OF COMBAT PHASE')
        self.resolve_combat()
        for player in self.players:
            self.current_player = player.player_num - 1
            self.combat_engine.attack_colony(player)
        print('END OF COMBAT PHASE')
        print('----------------------------------')

    def complete_turn(self):
        print('-------------------------------------------------')
        print('Turn', self.turns + 1)
        self.economic_engine.update_self(self.players)
        self.movement_engine.complete_movement_phase(self.players)
        self.complete_combat_phase()
        self.remove_dead_players()
        if self.complete is True:
            self.winner()
            return None
        self.economic_engine.complete_economic_phase()
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
        self.combat_engine.resolve_battles(occupants)
        # for o in occupants:
        #     if len(o) >= 2:
        #         self.combat_engine.check_for_battle(o)

    def find_combat_array(self):
        all_units = []
        for player in self.players:
            for unit in player.units:
                all_units.append(unit)
        occupants = self.board.occupy(all_units)
        return self.combat_engine.generate_combat_state(occupants)
    
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