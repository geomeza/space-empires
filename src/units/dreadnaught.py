from units.unit import Unit 

class Dreadnaught(Unit):
    cost = 25
    class_type = 'A'
    strength = 6
    defense = 3
    tactics = 5
    abbr = 'DR'
    name = 'Dreadnaught'
    armor = 3
    speed = 1
    hull_size = 3
    ship_size_needed = 6
    movement = 1

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength = self.strength + tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.movement = tech_lvls['move']
        self.maint = 3