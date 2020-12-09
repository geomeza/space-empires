from units.unit import Unit 

class Destroyer(Unit):
    cost = 9
    class_type = 'D'
    strength = 4
    defense = 0
    class_num = 2
    abbr = 'DE'
    name = 'Destroyer'
    armor = 1
    speed = 1
    hull_size = 1
    build_size = 2

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength = self.strength + tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.maint = 1