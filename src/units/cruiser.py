from units.unit import Unit 

class Cruiser(Unit):
    cost = 12
    class_type = 'C'
    strength = 4
    defense = 1
    tactics = 3
    abbr = 'C'
    name = 'Cruiser'
    armor = 2
    hull_size = 3
    maint = 3
    ship_size_needed = 2
    movement = 1

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength += tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.movement = tech_lvls['move']
        self.maint = 3