from units.unit import Unit 

class Colony(Unit):
    strength = 0
    speed = 0
    strength = 0
    name = 'Colony'
    class_num = 0
    defense = 1
    capacity = 3
    
    def __init__(self, coords, player, name, unit_num, colony_type = 'Colony'):
        super().__init__( coords, player, name, unit_num)
        self.base = None
        self.shipyards = []
        self.shipyard_count = 0
        self.builders = 0
        self.colony_type = colony_type