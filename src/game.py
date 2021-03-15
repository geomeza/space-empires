from player import Player
from board import Board
from engines.movement_engine import MovementEngine
from utility import Utility
from engines.economic_engine import EconomicEngine
from engines.combat_engine import CombatEngine
from logger import Logger
import sys


class Game:

    def __init__(self, **kwargs):
        self.justin_is_weird = False
        self.logger = None
        self.level = 0
        self.filename = None
        self.invalidation = True
        self.players = []
        self.dead_players = []
        self.current_player = 'None'
        self.board_size = [5,5]
        self.board = None
        self.planets = []
        self.turn_count = 1
        self.max_turns = 100
        self.phase = 'Bruh Moment'
        self.winner = 'None'
        self.logging = True
        self.dice_rolls = 'descending'
        self.complete = False
        self.scouts_only = False
        self.movement_rounds = 3
        self.banned_phases = []
        self.screens = False
        self.max_dice = 10
        self.default = False
        self.shipyards_cleared = True
        self.__dict__.update(kwargs)
        self.check_level()
        self.death_order = []
        if self.filename is not None:
            self.logger = Logger(self.filename)

    def check_level(self):
        if self.level > 0:
            if self.level == 1:
                self.max_turns = 20
                self.planets = []
                self.scouts_only = True
                self.banned_phases = ['economic']
                self.movement_rounds = 1
                self.screens = False
                self.shipyards_cleared = False
            if self.level == 2:
                self.max_turns = 20
                self.planets = []
                self.scouts_only = True
                self.banned_phases = []
                self.movement_rounds = 1
                self.screens = False
                self.shipyards_cleared = True
            if self.level == 3:
                self.max_turns = 100
                self.planets = []
                self.scouts_only = True
                if self.justin_is_weird:
                    self.banned_phases = ['economic']
                    self.max_turns = 6
                else:
                    self.banned_phases = []
                self.board_size = [7,7]
                self.movement_rounds = 3
                self.screens = False
                self.shipyards_cleared = True

    def log(self, string):
        if self.logger is not None:
            self.logger.log(string)
        if self.logging:
            print(string)


    def add_player(self, strategy, coords):
        new_player = Player(strategy, len(self.players), coords, self)
        self.players.append(new_player)

    def create_assets(self, planets):
        # self.log('Creating Board')
        self.board = Board(self.board_size, self, planets)
        self.utility = Utility(True, self)
        self.economic_engine = EconomicEngine(self.board, self)
        self.movement_engine = MovementEngine(self.board, self)
        self.combat_engine = CombatEngine(self.board, self)

    def initialize_game(self):
        self.create_assets(self.planets)
        # self.log('Initializing Players')
        for player in self.players:
            player.cp = 0
            player.initialize_units()
        self.board.update(self.players)
        # for s in range(len(self.players)):
            # self.log('----------------------------------')
            # self.log('Player '+str( s + 1)+ ':')
            # self.log('Combat Points: '+ str(self.players[s].cp))
            # self.show_unit_coords(s+1)
            # self.log('----------------------------------')

    def show_unit_coords(self):
        self.log('\n')
        for player in self.players:
            for unit in player.units:
                if unit.alt_name == 'Homeworld' and unit.alive:
                    self.log('\t\tPlayer '+str(unit.player.player_num + 1)+' '+'Homeworld' +' '+str(
                            unit.unit_num)+ ': '+ str(tuple(unit.coords)))
                elif unit.alive:
                    self.log('\t\tPlayer '+str(unit.player.player_num + 1)+' '+str(unit.name) +' '+str(
                            unit.unit_num)+ ': '+ str(tuple(unit.coords)))
            self.log('\n')

    def adjust_starting_and_colony_income(self, starting, colony_income):
        for player in self.players:
            player.cp = 10
            for unit in player.units:
                if unit.name == 'Colony':
                    unit.capacity = 20

    def complete_turn(self):
        self.death_order = []
        self.first_colony_destroyed = None
        if self.turn_count < self.max_turns:
            # self.log('TURN '+ str(self.turn_count))
            # self.log('------------------------------------------------------')
            if self.turn_count == 1 and self.level == 2:
                self.adjust_starting_and_colony_income(10,20)
                self.complete_economic_phase()
                self.banned_phases = ['economic']
            if 'movement' not in self.banned_phases:
                self.complete_movement_phase()
            self.remove_dead_players()
            if self.complete:
                return
            if 'combat' not in self.banned_phases:
                self.complete_combat_phase()
            self.remove_dead_players()
            if self.complete:
                return
            if 'economic' not in self.banned_phases:
                self.complete_economic_phase()
            self.turn_count += 1
            # self.log('------------------------------------------------------')
        else:
            self.complete = True
            if self.default:
                self.default_win()
                self.log('--------------------------------------')
                self.log('Player '+str(self.winner.player_num)+ ' Won By Default')
                self.log('--------------------------------------')
                self.close()
            else:
                if not self.justin_is_weird:
                    self.winner = len(self.players) + 5
                    self.winner_name = 'TIE'
                    self.log('--------------------------------------')
                    self.log('MAX TURNS REACHED')
                    self.log('TIE GAME')
                    self.log('--------------------------------------')
                    self.close()
                else: 
                    self.close()

    def complete_movement_phase(self):
        self.movement_engine.complete_movement_phase()

    def complete_combat_phase(self):
        self.combat_engine.complete_combat_phase()

    def complete_economic_phase(self):
        self.economic_engine.complete_economic_phase()

    def complete_many_turns(self, num_turns):
        for _ in range(num_turns):
            self.complete_turn()
            if self.complete:
                return

    def run_until_complete(self):
        while True:
            self.complete_turn()
            if self.complete:
                break

    def remove_dead_players(self):
        dead_players = []
        for player in self.players:
            colonized_bool = player.home_planet.colonized
            colony = player.home_planet.colony
            if colonized_bool is False and colony is None:
                dead_players.append(player)
                for unit in player.units:
                    unit.destroy()
        for player in dead_players:
            self.players.remove(player)
            self.log('--------------------------------------')
            self.log('Player '+ str(player.player_num) + ' Has Died')
            self.log('--------------------------------------')
        if len(self.players) == 1:
            player = self.players[0]
            self.winner_name = player.strategy.name
            self.winner = player.player_num
            self.complete = True
            self.log('--------------------------------------')
            self.log('Player '+ str(player.player_num)+ ' Won')
            self.log('--------------------------------------')
            self.close()
        elif len(self.players) == 0:
            player_name = self.death_order[-1][1]
            player_num = self.death_order[-1][0]
            self.winner_name = player_name
            self.winner = player_num
            self.complete = True
            self.log('--------------------------------------')
            self.log('Player '+ str(player_num)+ ' Won')
            self.log('--------------------------------------')
            self.close()


    def close(self):
        if self.filename is not None:
            self.logger.close_file()
            return

    def default_win(self):
        units = [len(player.units) for player in self.players]
        self.winner = self.players[units.index(max(units))]
        self.winner_name = self.winner.strategy.name

    def game_state(self):
        state = {}
        state['board_size'] = self.board.size
        state['turn'] = self.turn_count
        state['phase'] = self.phase
        state['round'] = self.movement_engine.movement_phase
        state['player_whose_turn'] = self.current_player
        state['players'] = [self.player_state(
            player) for player in self.players]
        state['planets'] = [planet.coords for planet in self.board.planets]
        state['unit_data'] = {
        'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5, 'tactics': 5, 'attack': 5, 'defense': 2, 'maintenance': 3},
        'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4, 'tactics': 4, 'attack': 5, 'defense': 1, 'maintenance': 2},
        'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 3, 'tactics': 3, 'attack': 4, 'defense': 1, 'maintenance': 2},
        'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2, 'tactics': 2, 'attack': 4, 'defense': 0, 'maintenance': 1},
        'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6, 'tactics': 5, 'attack': 6, 'defense': 3, 'maintenance': 3},
        'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 1, 'attack': 3, 'defense': 0, 'maintenance': 1},
        'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 3, 'attack': 3, 'defense': 0, 'maintenance': 0},
        'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
        'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
        'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2, 'tactics': 5, 'attack': 7, 'defense': 2, 'maintenance': 0}
    }
        state['technology_data'] = {
            'shipsize': [0, 10, 15, 20, 25, 30],
            'attack': [20, 30, 40],
            'defense': [20, 30, 40],
            'movement': [0, 20, 30, 40, 40, 40],
            'shipyard': [0, 20, 30]}
        state['winner'] = self.winner
        return state

    def player_state(self, player):
        state = {}
        state['home_coords'] = player.home_coords
        state['player_num'] = player.player_num
        translations = ['ss', 'atk', 'def', 'move', 'shpyrd']
        techs = ['shipsize', 'attack', 'defense', 'movement', 'shipyard']
        state['technology'] = {techs[translations.index(
            tech)]: player.tech_lvls[tech] for tech in player.tech_lvls.keys()}
        state['cp'] = player.cp
        state['units'] = [self.unit_state(unit) for unit in player.units]
        return state

    def hidden_player_state(self,player, wanted = None):
        state = {}
        state['home_coords'] = player.home_coords
        state['player_num'] = player.player_num
        state['units'] = [{'coords': unit.coords, 'num': unit.unit_num} for unit in player.units]
        return state

    def hidden_combat_player_state(self, player, units_in_combat):
        units_in_combat = [unit.unit_num for unit in units_in_combat if unit.player.player_num == player.player_num]
        state = {}
        state['home_coords'] = player.home_coords
        state['player_num'] = player.player_num
        state['units'] = [self.unit_state(unit) if unit.unit_num in units_in_combat else {'coords': unit.coords, 'num': unit.unit_num} for unit in player.units]
        return state


    def hidden_game_state(self, wanted = None):
        state = {}
        state['board_size'] = self.board.size
        state['turn'] = self.turn_count
        state['phase'] = self.phase
        state['round'] = self.movement_engine.movement_phase
        state['player_whose_turn'] = self.current_player
        state['players'] = [self.player_state(
            player) if player.player_num == wanted else self.hidden_player_state(player) for player in self.players]
        state['unit_data'] = {
            'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5},
            'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4},
            'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 2},
            'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2},
            'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6},
            'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1},
            'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1},
            'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1},
            'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1},
            'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2}}
        state['technology_data'] = {
            'shipsize': [0, 10, 15, 20, 25, 30],
            'attack': [20, 30, 40],
            'defense': [20, 30, 40],
            'movement': [0, 20, 30, 40, 40, 40],
            'shipyard': [0, 20, 30]}
        state['winner'] = self.winner
        return state

    def hidden_game_state_for_combat(self, wanted = None, units = None):
        state = {}
        state['board_size'] = self.board.size
        state['turn'] = self.turn_count
        state['phase'] = self.phase
        state['round'] = self.movement_engine.movement_phase
        state['player_whose_turn'] = self.current_player
        state['players'] = [self.player_state(
            player) if player.player_num == wanted else self.hidden_combat_player_state(player, units) for player in self.players]
        state['unit_data'] = {
            'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5},
            'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4},
            'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 2},
            'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2},
            'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6},
            'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1},
            'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1},
            'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1},
            'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1},
            'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2}}
        state['technology_data'] = {
            'shipsize': [0, 10, 15, 20, 25, 30],
            'attack': [20, 30, 40],
            'defense': [20, 30, 40],
            'movement': [0, 20, 30, 40, 40, 40],
            'shipyard': [0, 20, 30]}
        state['winner'] = self.winner
        return state


    def unit_state(self, unit):
        state = {}
        state['player'] = unit.player.player_num
        state['type'] = unit.name
        state['tactics'] = unit.tactics
        state['num'] = unit.unit_num
        state['coords'] = unit.coords
        state['maint'] = unit.maint
        state['alive'] = unit.alive
        translations = ['atk', 'def', 'move']
        techs = ['attack', 'defense', 'movement']
        state['technology'] = {techs[translations.index(
            tech)]: unit.tech_lvls[tech] for tech in unit.tech_lvls.keys()}
        state['hits_left'] = unit.armor
        state['turn_created'] = unit.turn_created
        return state
