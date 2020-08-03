from units.unit import Unit 

class Base(Unit):
    class_type = 'A'
    hull_size = 2
    class_num = 5
    strength = 7
    defense = 2
    armor = 3
    cost = 12
    name = 'Base'
    abbr = 'B'
    
    def __init__(self, coords, player, name, unit_num, colony):
        super().__init__( coords, player, name, unit_num)
        self.colony = colony