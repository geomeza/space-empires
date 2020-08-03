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
import random

class CombatEngine:

    def __init__(self, board):
        self.units = []
        self.battle_order = []
        self.enemies = []
        self.team_units = []
        self.game_board = board
        self.dice = 1

    def attack_colony(self, player):
        for unit in player.units:
            space = self.game_board.grid[tuple(unit.coords)]
            if space.planet is not None:
                if space.planet.player != player:
                    if space.planet.colonized is True:
                        if space.colony.base is not None:
                            print('----------------------------------')
                            print('Combat At',unit.coords)
                            print('Player', unit.player.player_num, unit.name)
                            print('VS')
                            print('Player', space.colony.player.player_num, 'Base')
                            self.duel_with_base(unit, space.colony.base)
                        else:
                            print('----------------------------------')
                            print('Player',unit.player.player_num,'Encountered Player', space.colony.player.player_num, 'Colony')
                            self.colony_shot(unit, space.planet.colony)
        return None

    def colony_shot(self, unit1, colony):
        threshold = unit1.strength - 3
        dice_roll = random.randint(1,6)
        if dice_roll <= threshold:
            print('Colony Destroyed')
            space = self.game_board.grid[tuple(colony.coords)]
            space.planet.colonized = False
            space.planet.player = None
            space.planet.colony = None
            space.colony = None
            colony.player.destroy_colony(colony, space.planet, space)
        else:
            print('Colony Missed')

    def supremacy(self, units):
        for i in range(len(units)):
            for j in range(i + 1, len(units)):
                unit1 = units[i]
                unit2 = units[j]
                u1_tactics = unit1.player.tech_lvls[0] + unit1.player.tech_lvls[1]
                u2_tactics = unit2.player.tech_lvls[0] + unit2.player.tech_lvls[1]
                if (unit1.class_num + u1_tactics) > (unit2.class_num + u2_tactics):
                    units[i], units[j] = units[j], units[i]
        return units

    def sort(self, units, player):
        self.units = units
        self.enemies = []
        self.team_units = []
        for unit in units:
            if unit.player == player:
                self.team_units.append(unit)
            else:
                self.enemies.append(unit)
        return None

    def hit_threshold(self, attacker, defender):
        return attacker.strength - defender.defense

    def class_supremacy(self, attacker, defender):
        a_tactics = attacker.player.tech_lvls[0] + attacker.player.tech_lvls[1]
        d_tactics = defender.player.tech_lvls[0] + defender.player.tech_lvls[1]
        attacker_rating = attacker.class_num + a_tactics
        defender_rating = defender.class_num + d_tactics
        if attacker_rating > defender_rating:
            return 1
        elif attacker_rating < defender_rating:
            return 2
        elif attacker_rating == defender_rating:
            return 1

    def duel_with_base(self, unit, base):
        first = self.class_supremacy(unit, base)
        fight_order = [unit, base]
        if first == 2:
            fight_order.reverse()
        while unit.alive == True and base.alive == True:
            threshold = self.hit_threshold(fight_order[0],fight_order[1]) 
            dice_roll = random.randint(1,6)
            if dice_roll <= threshold or dice_roll == 1:
                if fight_order[0].armor > 1:
                    print('------')
                    print('Player',fight_order[0].player.player_num, fight_order[0].name,'Was Hit!')
                    fight_order[0].armor -= 1
                    print('------')
                else:
                    print('------')
                    print('Player',fight_order[0].player.player_num, fight_order[0].name,' Was Destroyed!')
                    print('Survivor: Player', fight_order[1].player.player_num, ',',fight_order[1].name)
                    if fight_order[0].name == unit.name:
                        fight_order[0].destroy()
                    if fight_order[0].name == base.name:
                        space = self.game_board.grid[tuple(base.coords)]
                        planet = space.planet
                        colony = base.colony
                        base.player.destroy_colony(colony, planet, space)
                    return fight_order[1]
            else:
                print('------')
                print('Player',fight_order[0].player.player_num, fight_order[0].name,' Was Missed!')
                print('------')
            fight_order.reverse()

    def unit_shot(self, attacker, defender):
        first = self.class_supremacy(attacker,defender)
        fight_order = [attacker, defender]
        if first == 2:
            fight_order.reverse()
        print('-------------')
        print('Player',fight_order[1].player.player_num,fight_order[1].name,'Shoots At:')
        print('Player', fight_order[0].player.player_num, fight_order[0].name)
        threshold = self.hit_threshold(fight_order[1],fight_order[0]) 
        # dice_roll = random.randint(1,6)
        dice_roll = self.dice
        if dice_roll <= threshold or dice_roll == 1:
            if fight_order[0].armor > 1:
                print('------')
                print('Player',fight_order[0].player.player_num, fight_order[0].name,'Was Hit!')
                fight_order[0].armor -= 1
                print('------')
            else:
                print('------')
                print('Player',fight_order[0].player.player_num, fight_order[0].name,' Was Destroyed!')
                print('Survivor: Player', fight_order[1].player.player_num, ',',fight_order[1].name)
                self.units.remove(fight_order[0])
                fight_order[0].destroy()
                self.dice += 1
                if self.dice == 7:
                    self.dice = 1
                return fight_order[1]
        else:
            print('------')
            print('Player',fight_order[0].player.player_num, fight_order[0].name,' Was Missed!')
            print('------')
        self.dice += 1
        if self.dice == 7:
            self.dice = 1

    def check_battle_status(self, units):
        if len(units) >= 2:
            for unit in units:
                self.sort(units, unit.player)
                if len(self.enemies) == 0:
                    return True
            return False
        else:
            return True
 
    def preferred_unit(self, player):
        self.enemies = self.supremacy(self.enemies)
        return player.unit_preference(self.enemies)

    # def screen_units:
        
        
    def battle(self, units):
        status = self.check_battle_status(units)
        if status is False:
            print('--------------------------')
            remove_colony_ships = []
            print('Combat At', units[0].coords)
            for unit in units:
                if unit.name == 'Colony Ship':
                    print('---------------')
                    print('Player',unit.player.player_num,'Colony Ship Encountered Enemy')
                    print('Colony Ship Destroyed')
                    print('---------------')
                    unit.destroy()
                    remove_colony_ships.append(unit)
            for c in remove_colony_ships:
                units.remove(c)
            print('In Combat:')
            for unit in units:
                print('Player',unit.player.player_num,unit.name)
            self.units = units
            over = False
            while over is False:
                self.battle_order = self.supremacy(self.units)
                self.battle_order.reverse()
                for unit in self.battle_order:
                    self.sort(self.units, unit.player)
                    enemy = self.preferred_unit(unit.player)
                    self.unit_shot(unit, enemy)
                    status = self.check_battle_status(self.units)
                    if status is True:
                        over = True
                        print('-------------------')
                        print('The Battle Is Over!')
                        unit_choice = random.choice(self.units)
                        print('Player', unit_choice.player.player_num, 'Units Win')
                        print('-------------------')
                        print('--------------------------')
                        break
        else:
            return None  
