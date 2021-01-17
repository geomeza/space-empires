from units.unit import Unit 

class Battlecruiser(Unit):
    cost = 15
    class_type = 'B'
    strength = 5
    defense = 1
    class_num = 4
    abbr = 'BC'
    name = 'Battlecruiser'
    armor = 2
    speed = 1
    hull_size = 2
    ship_size_needed = 4
    movement = 1
    ship_size_needed = 4

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength = self.strength + tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.maint = 2