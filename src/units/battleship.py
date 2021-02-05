from units.unit import Unit 

class Battleship(Unit):
    cost = 20
    class_type = 'A'
    strength = 5
    defense = 2
    tactics = 5
    abbr = 'BS'
    name = 'Battleship'
    armor = 3
    speed = 1
    hull_size = 3
    ship_size_needed = 5
    movement = 1

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.strength = self.strength + tech_lvls['atk']
        self.defense += tech_lvls['def']
        self.maint = 3