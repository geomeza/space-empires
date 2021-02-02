import random


class CombatEngine:

    def __init__(self, board, game):
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
        ascending = [i for i in range(1,max_roll + 1)]
        descending = ascending[:]
        descending.reverse()
        return {'ascending': ascending, 'descending': descending, 'random': ascending}

    def roll_dice(self):
        if self.dice_rolls != 'random':
            if self.order < 9:
                self.order += 1
            else:
                self.order = 0
        else:
            self.order = random.randint(0, 9)
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

    def complete_combat_phase(self):
        self.game.phase = 'Combat'
        if self.game.logging:
            print('START OF COMBAT PHASE')
        battles = self.find_battles()
        for coords, units in battles.items():
            if self.game.logging:
                print('Battle at', coords)
            self.over = False
            self.battle(units)
            self.reset_stats()
            self.board.update(self.game.players)
        self.board.update(self.game.players)
        if self.game.logging:
            print('END OF COMBAT PHASE')

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

    def which_ship_to_attack(self, player, attacker, units):
        self.sort_units(units, player)
        unit_info = [self.game.unit_state(unit)
                     for unit in self.enemies if unit.alive]
        units = [unit for unit in units if unit.alive]
        decision = player.strategy.decide_which_unit_to_attack(
            self.get_combat_state(), tuple(attacker.coords), units.index(attacker))
        psuedo_ship = self.get_combat_state()[tuple(attacker.coords)][decision]
        chosen_enemy = None
        for unit in units:
            if unit.unit_num == psuedo_ship['unit'] and unit.player.player_num == psuedo_ship['player']:
                chosen_enemy = unit
        return chosen_enemy

    def hit_threshold(self, attacker, defender):
        return (attacker.strength + attacker.tech_lvls['atk']) - (defender.defense + defender.tech_lvls['def'])

    def supremacy(self, units):
        for i in range(len(units)):
            for j in range(i + 1, len(units)):
                unit1 = units[i]
                unit2 = units[j]
                u1_tactics = unit1.player.tech_lvls['atk'] + \
                    unit1.tech_lvls['atk']
                u2_tactics = unit2.player.tech_lvls['atk'] + \
                    unit2.tech_lvls['atk']
                if (unit1.class_num + u1_tactics) < (unit2.class_num + u2_tactics):
                    units[i], units[j] = units[j], units[i]
                elif (unit1.class_num + u1_tactics) == (unit2.class_num + u2_tactics):
                    if unit1.player.player_num > unit2.player.player_num:
                        units[i], units[j] = units[j], units[i]
        return units

    def unit_shot(self, attacker, defender):
        self.roll_dice()
        hit_threshold = self.hit_threshold(attacker, defender)
        if self.game.logging:
            print('-------')
            print('Player', attacker.player.player_num, attacker.name, attacker.unit_num,
                  'Shoots at', 'Player', defender.player.player_num, defender.name, defender.unit_num)
            print('Threshold:', hit_threshold)
            print('Player', attacker.player.player_num,
                  'Rolled A', self.dice_roll)
        if self.dice_roll <= hit_threshold or self.dice_roll == 1:
            if self.game.logging:
                print('They Hit')
            defender.hit()
            if not defender.alive:
                self.dead_ships.append(defender)
                if self.game.logging:
                    print(defender.name, 'Destroyed')
        else:
            if self.game.logging:
                print('They Miss')
                print('-------')

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
            if self.game.logging:
                print('In Combat:')
                for unit in self.battle_order:
                    print('Player', unit.player.player_num,
                          unit.name, unit.unit_num)
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
                                unit_choice = self.units[0]
                                if self.game.logging:
                                    print('Battle Is Over')
                                    print(
                                        'Player', unit_choice.player.player_num, 'Units Win!')
                                    print('Survivors')
                                    print('------------------------')
                                    for unit in self.units:
                                        if unit.alive:
                                            print(unit.name, unit.unit_num)
                                    print('------------------------')
                                return
                self.units = self.remove_dead_ships(self.units)

    def colonize(self):
        planet_coords = [planet.coords for planet in self.board.planets]
        self.board.update(self.game.players)
        for player in self.game.players:
            for unit in player.units:
                if unit.name == 'Colony Ship':
                    if unit.coords in planet_coords:
                        planet = self.board.grid[tuple(unit.coords)].planet
                        if not planet.colonized:
                            if player.strategy.will_colonize_planet(unit.coords, self.game.hidden_game_state(player.player_num)):
                                player.build_colony(
                                    unit.coords, col_type='Normal', colony_ship=unit)
                                if self.game.logging:
                                    print('Player', player.player_num,
                                          'colonized a planet at', unit.coords)

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
            unit_dicts = [{'player_index': unit.player.player_num,
                           'unit': unit.unit_num,
                             'type' : unit.name,
                            'technology' : {techs[translations.index(
                              tech)]: unit.tech_lvls[tech] for tech in unit.tech_lvls.keys()},
                            'hits_left': unit.armor,
                            'turn_created' : unit.turn_created} for unit in ordered_units]
            state.update({coords: unit_dicts})
        return state

    # def screen_units(self, units):
    #     players = set([unit.player for unit in units])
    #     counts = {player: }