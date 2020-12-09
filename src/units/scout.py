from units.unit import Unit 

class Scout(Unit):
    cost = 6
    class_type = 'E'
    strength = 3
    defense = 0
    class_num = 1
    abbr = 'S'
    name = 'Scout'
    armor = 1
    hull_size = 1
    maint = 1
    build_size = 1

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength = self.strength + tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.maint = 1