from player import Player
from board import Board
from movement_engine import MovementEngine
from utility import Utility
from economic_engine import EconomicEngine
from combat_engine import CombatEngine

class Game:

    def __init__(self, board_size = [5,5], planets = [[1,0]],max_turns = 10, logging = True, die_rolls = 'descending'):
        self.players = []
        self.dead_players = []
        self.current_player = 'None'
        self.board_size = board_size
        self.board = None
        self.planets = planets
        self.turn_count = 0
        self.max_turns = max_turns
        self.phase = 'Bruh Moment'
        self.winner = 'None'
        self.logging = logging
        self.dice_rolls = die_rolls
        self.complete = False

    def add_player(self, strategy, coords):
        new_player = Player(strategy, len(self.players), coords, self)
        self.players.append(new_player)

    def create_assets(self, planets):
        if self.logging:
            print('Creating Board')
        self.board = Board(self.board_size, self, planets)
        self.utility = Utility(True, self)
        self.economic_engine = EconomicEngine(self.board, self)
        self.movement_engine = MovementEngine(self.board, self)
        self.combat_engine = CombatEngine(self.board, self)

    def initialize_game(self):
        self.create_assets(self.planets)
        if self.logging:
            print('Initializing Players')
        for player in self.players:
            player.cp = 0
            player.initialize_units()
        self.board.update(self.players)
        if self.logging:
            for s in range(len(self.players)):
                print('----------------------------------')
                print('Player', s + 1, ':')
                print('Combat Points:',self.players[s].cp)
                self.show_unit_coords(s+1)
                print('----------------------------------')

    def show_unit_coords(self, player_num):
        for unit in self.players[player_num - 1].units:
            print(unit.name, ':', unit.coords)

    def complete_turn(self):
        self.turn_count += 1
        self.complete_movement_phase()
        self.complete_combat_phase()
        self.remove_dead_players()
        if self.complete:
            return
        self.complete_economic_phase()

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
            if self.logging:
                print('--------------------------------------')
                print('Player', player.player_num, 'Has Died')
                print('--------------------------------------')
        if len(self.players) == 1:
            player = self.players[0]
            self.winner = player.player_num
            self.complete = True
            print('--------------------------------------')
            print('Player', player.player_num,'Won')
            print('--------------------------------------')




    def game_state(self):
        state = {}
        state['board_size'] = self.board.size
        state['turn'] = self.turn_count
        state['phase'] = self.phase
        state['player_whose_turn'] = self.current_player
        state['players'] = [self.player_state(player) for player in self.players]
        state['planets'] = [planet.coords for planet in self.board.planets]
        state['unit_data'] = {
            'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed' : 5},
            'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed' : 4},
            'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed' : 2},
            'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed' : 2},
            'Dreadnaught': {'cp_cost': 24, 'hullsize': , 'shipsize_needed' : 6},
            'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed' : 1},
            'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed' : 1},
            'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed' : 1},
            'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed' : 1},
            'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed' : 2}}
        state['technology_data'] = {
            'shipsize': [10, 15, 20, 25, 30],
            'attack': [20, 30, 40],
            'defense': [20, 30, 40],
            'movement': [20, 30, 40, 40, 40],
            'shipyard': [20, 30]}
        state['winner'] = self.winner
        return state

    def player_state(self, player):
        state = {}
        state['home_coords'] = player.home_coords
        state['player_num'] = player.player_num
        translations = ['ss', 'atk', 'def', 'move', 'shpyrd']
        techs = ['shipsize', 'attack', 'defense', 'movement', 'shipyard']
        state['tech'] = {techs[translations.index(tech)] : player.tech_lvls[tech] for tech in player.tech_lvls.keys()}
        state['cp'] = player.cp
        state['units'] = [self.unit_state(unit) for unit in player.units]
        return state

    def unit_state(self, unit):
        state = {}
        state['player'] = unit.player.player_num
        state['type'] = unit.name
        state['class_num'] = unit.class_num
        state['unit_num'] = unit.unit_num
        state['coords'] = unit.coords
        state['maint'] = unit.maint
        translations = ['atk', 'def', 'move']
        techs = ['attack', 'defense', 'movement']
        state['tech'] = {techs[translations.index(tech)] : unit.tech_lvls[tech] for tech in unit.tech_lvls.keys()}
        state['hits_left'] = unit.armor
        state['turn_created'] = unit.turn_created
        return state
