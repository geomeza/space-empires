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

    def add_player(self, strategy, coords):
        new_player = Player(strategy, len(self.players) + 1, coords, self)
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
        self.complete_economic_phase()

    def complete_movement_phase(self):
        self.movement_engine.complete_movement_phase()

    def complete_combat_phase(self):
        self.combat_engine.complete_combat_phase()
    
    def complete_economic_phase(self):
        self.economic_engine.complete_economic_phase()

    def complete_many_turns(self, num_turns):
        for i in range(num_turns):
            self.complete_turn()

    def game_state(self):
        state = {}
        state['board_size'] = self.board.size
        state['turn'] = self.turn_count
        state['phase'] = self.phase
        state['current_player'] = self.current_player
        state['players'] = [self.player_state(player) for player in self.players]
        state['planets'] = [planet.coords for planet in self.board.planets]
        state['winner'] = self.winner
        return state

    def player_state(self, player):
        state = {}
        state['player num'] = player.player_num
        state['tech'] = player.tech_lvls
        state['cp'] = player.cp
        state['units'] = [self.unit_state(unit) for unit in player.units]
        return state

    def unit_state(self, unit):
        state = {}
        state['player'] = unit.player.player_num
        state['name'] = unit.name
        state['class num'] = unit.class_num
        state['unit num'] = unit.unit_num
        state['coords'] = unit.coords
        state['maint'] = unit.maint
        state['tech'] = unit.tech_lvls
        state['hits left'] = unit.armor
        state['turn created'] = unit.turn_created
        return state
