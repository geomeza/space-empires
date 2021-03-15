import random
import math


class CombatEngine:

    def __init__(self, board, game):
        self.seed = None
        self.board = board
        self.game = game
        self.battles = []
        self.team = []
        self.enemies = []
        self.battle_order = []
        self.dead_ships = []
        self.dice_rolls = self.game.dice_rolls
        self.dice = self.make_dice()
        self.order = -1
        self.dice_roll = 0
        self.combat_state = None

    def make_dice(self):
        max_roll = self.game.max_dice
        ascending = [i for i in range(1, max_roll + 1)]
        descending = ascending[:]
        descending.reverse()
        if isinstance(self.game.dice_rolls, list):
            self.dice_rolls = 'custom'
            self.game.max_dice = len(self.game.dice_rolls)
            return {'custom': self.game.dice_rolls}
        return {'ascending': ascending, 'descending': descending, 'random': ascending}

    def roll_dice(self):
        if self.dice_rolls != 'random':
            if self.order < self.game.max_dice - 1:
                self.order += 1
            else:
                self.order = 0
        else:
            self.dice_roll = math.ceil(10*random.random())
            return
        self.dice_roll = self.dice[self.dice_rolls][self.order]

    def find_battles(self):
        potential_battles = self.board.get_all_units_and_coords()
        passives = {}
        for coords, units in potential_battles.items():
            self.reset_stats()
            self.sort_units(units, units[0].player)
            if len(self.enemies) == 0:
                passives.update({coords: units})
            self.reset_stats()
        for coords, units in passives.items():
            del potential_battles[coords]
        self.combat_state = potential_battles
        return potential_battles

    def remove_colony(self, units):
        colony = None
        colony_shipyards = None
        for unit in units:
            if unit.name == 'Colony':
                colony = unit
                colony_shipyards = unit.shipyards
        if colony is None:
            return units
        enem_units = [(unit.name, unit.player.player_num) for unit in units if unit.player.player_num ==
                      colony.player.player_num and unit.alive and unit.name != 'Colony']
        if len(colony_shipyards) > 0 or len(enem_units) > 0:
            if colony in units:
                units.remove(colony)
            return units
        else:
            return units

    def complete_combat_phase(self):
        self.game.phase = 'Combat'
        self.game.log('\nBEGINNING OF TURN ' +
                      str(self.game.turn_count) + ' COMBAT PHASE')
        battles = self.find_battles()
        while len(battles) > 0:
            self.log_battles(battles)
            for coords, units in battles.items():
                self.game.log('\n\tCombat at ' + str(coords))
                self.over = False
                self.battle(self.remove_colony(units))
                self.reset_stats()
                self.board.update(self.game.players)
            self.board.update(self.game.players)
            battles = self.find_battles()
        self.game.movement_engine.reset_attacking_vars()
        self.game.log('\nEND OF TURN ' +
                      str(self.game.turn_count) + ' COMBAT PHASE')

    def log_battles(self, battles):
        self.game.log('\n\tCombat Locations:')
        for coords, units in battles.items():
            self.game.log('\n\t\t'+str(coords))
            self.game.log('\n')
            sorted_units = self.supremacy(self.remove_colony(units))
            for unit in sorted_units:
                self.game.log('\t\t\tPlayer '+str(unit.player.player_num + 1)+' '+str(unit.name) + ' '+str(
                    unit.unit_num))

    def sort_units(self, units, player):
        self.enemies = []
        self.team = []
        self.units = units
        for unit in self.units:
            if unit.alive:
                if unit.player == player:
                    self.team.append(unit)
                else:
                    self.enemies.append(unit)

    def reset_stats(self):
        self.units = []
        self.battle_order = []
        self.enemies = []
        self.team = []
        self.dead_ships = []

    def check_battle_status(self, units):
        units = [unit for unit in units if unit.alive]
        self.over = False
        if len(units) >= 2:
            self.sort_units(units, units[0].player)
            if len(self.enemies) > 0:
                self.over = False
                return
            self.over = True
            return
        else:
            self.over = True
            return

    def get_ship_from_decision(self, unit_type, unit_num, player, units):
        enem_units = [unit for unit in units if unit.player != player]
        for unit in enem_units:
            if unit_type == unit.name:
                if unit.unit_num == unit_num:
                    return unit

    def which_ship_to_attack(self, player, attacker, units):
        self.sort_units(units, player)
        unit_info = [self.game.unit_state(unit)
                     for unit in self.enemies if unit.alive]
        units = [unit for unit in units if unit.alive]
        # NONE IS PLACEHOLDER FOR HIDDEN COMBAT GAME STATE
        decision = player.strategy.decide_which_unit_to_attack(
            self.get_combat_state(), self.game.hidden_game_state_for_combat(player.player_num, units), tuple(attacker.coords), attacker.name, units.index(attacker))
        # psuedo_ship = self.get_combat_state()[tuple(attacker.coords)][decision]
        chosen_enemy = self.get_ship_from_decision(
            decision[0], decision[1], player, units)
        # for unit in units:
        #     if unit.unit_num == psuedo_ship['unit'] and unit.player.player_num == psuedo_ship['player']:
        #         chosen_enemy = unit
        #         return chosen_enemy
        return chosen_enemy

    def hit_threshold(self, attacker, defender):
        return (attacker.strength + attacker.tech_lvls['atk']) - (defender.defense + defender.tech_lvls['def'])

    def supremacy(self, units):
        sorted_units = sorted(units, key=lambda unit: (
            unit.tactics, not unit.attacking, -1*unit.unit_num), reverse=True)
        return sorted_units

    def unit_shot(self, attacker, defender):
        self.roll_dice()
        hit_threshold = self.hit_threshold(attacker, defender)
        # self.game.log('-------')
        self.game.log('\n')
        self.game.log('\t\tAttacker: Player ' + str(attacker.player.player_num +
                                                    1) + " " + attacker.name+" " + str(attacker.unit_num))
        self.game.log('\t\tDefender: Player ' + str(defender.player.player_num +
                                                    1) + " " + defender.name + " " + str(defender.unit_num))
        # self.game.log('Threshold: '+ str(hit_threshold))
        self.game.log('\t\tDie Roll: ' + str(self.dice_roll))
        if self.dice_roll <= hit_threshold or self.dice_roll == 1:
            self.game.log('\t\tHit!')
            defender.hit()
            if not defender.alive:
                self.dead_ships.append(defender)
                self.game.log('\t\tPlayer ' + str(defender.player.player_num+1) + " " +
                              defender.name + " " + str(defender.unit_num) + ' was destroyed')
                # self.game.log('-------')
        else:
            self.game.log('\t\t(Miss)')
            # self.game.log('-------')

    def remove_non_fighters(self, units):
        passives = []
        for unit in units:
            if unit.name == 'Colonyship' or unit.name == 'Decoy':
                passives.append(unit)
        if len(passives) == len(units):
            self.over = True
            return units
        else:
            for passive in passives:
                units.remove(passive)
                passive.destroy()
            status = self.check_battle_status(units)
            return units

    def remove_dead_ships(self, units):
        self.units = units
        for unit in units:
            if unit in self.dead_ships:
                self.units.remove(unit)
        return self.units

    def battle(self, units):
        units = self.remove_non_fighters(units)
        if self.over:
            return
        else:
            self.over = False
            self.units = units
            self.battle_order = self.supremacy(self.units)
            # self.game.log('In Combat:')
            # for unit in self.battle_order:
            #     self.game.log('Player '+ str(unit.player.player_num)+ " "+
            #             unit.name+ " "+ str(unit.unit_num))
            while not self.over:
                self.battle_order = self.supremacy(self.units)
                self.units = self.battle_order
                for unit in self.battle_order:
                    if unit.alive:
                        if not unit.can_atk:
                            continue
                        self.sort_units(units, unit.player)
                        enem = self.which_ship_to_attack(
                            unit.player, unit, self.units)
                        self.unit_shot(unit, enem)
                        self.check_battle_status(self.units)
                        if self.over:
                            if len(self.units) >= 1:
                                self.remove_dead_ships(self.units)
                                # unit_choice = self.units[0]
                                # self.game.log('Battle Is Over')
                                # self.game.log(
                                #     'Player '+ str(unit_choice.player.player_num)+ ' Units Win!')
                                # self.game.log('Survivors')
                                # self.game.log('------------------------')
                                # for unit in self.units:
                                #     if unit.alive:
                                #         self.game.log(unit.name+ str(unit.unit_num))
                                # self.game.log('------------------------')
                                return
                self.units = self.remove_dead_ships(self.units)

    def colonize(self, coords):
        planet_existant = self.check_grid_for_planet(coords)
        if planet_existant:
            self.board.update(self.game.players)
            planet = self.board.grid[tuple(coords)].planet
            board_space = self.board.grid[tuple(coords)]
            if not planet.colonized:
                for unit in board_space.units:
                    if unit.name == 'Colonyship':
                        if player.strategy.will_colonize_planet(unit.coords, self.game.hidden_game_state(player.player_num)):
                            player.build_colony(
                                unit.coords, col_type='Normal', colony_ship=unit)
                            self.game.log('Player ' + str(player.player_num) +
                                          ' colonized a planet at ' + str(unit.coords))
        else:
            return

    def check_grid_for_planet(self, coords):
        planet_coords = [planet.coords for planet in self.board.planets]
        if coords in planet_coords:
            return True

    def attack_colony(self):
        planet_coords = [planet.coords for planet in self.board.planets]
        self.board.update(self.game.players)
        for player in self.game.players:
            for unit in player.units:
                if unit.coords in planet_coords:
                    planet = self.board.grid[tuple(unit.coords)].planet
                    if planet.colonized:
                        if unit.can_atk and planet.colony.player != unit.player:
                            self.unit_shot(
                                attacker=unit, defender=planet.colony)

    def get_combat_state(self):
        state = {}
        for coords, units in self.combat_state.items():
            translations = ['atk', 'def', 'move']
            techs = ['attack', 'defense', 'movement']
            ordered_units = self.supremacy(units)
            ordered_units = [unit for unit in ordered_units if unit.alive]
            unit_dicts = [{'player': unit.player.player_num,
                           'num': unit.unit_num,
                           'type': unit.name,
                           'technology': {techs[translations.index(
                               tech)]: unit.tech_lvls[tech] for tech in unit.tech_lvls.keys()},
                           'hits_left': unit.armor,
                           'turn_created': unit.turn_created} for unit in ordered_units]
            state.update({coords: unit_dicts})
        return state

    # def screen_units(self, units):
    #     players = set([unit.player for unit in units])
    #     counts = {player: }

    def check_occupace(self, coords):
        space_units = self.board.get_space_units(coords)
        passives = False
        self.reset_stats()
        self.sort_units(space_units, space_units[0].player)
        if len(space_units) == 1 or len(self.enemies) == 0:
            passives = True
        self.reset_stats()
        if not passives:
            for unit in space_units:
                if unit.can_atk and unit.moveable:
                    unit.moveable = False
                    unit.brought_into_fight = True
