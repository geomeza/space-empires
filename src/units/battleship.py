from units.unit import Unit 

class Battleship(Unit):
    cost = 20
    class_type = 'A'
    strength = 5
    defense = 2
    class_num = 5
    abbr = 'BS'
    name = 'Battleship'
    armor = 3
    speed = 1
    hull_size = 3
    build_size = 5

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength = self.strength + tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.maint = 3