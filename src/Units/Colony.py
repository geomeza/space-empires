from Units.Unit import Unit 

class Colony(Unit):
    strength = 0
    speed = 0
    strength = 0
    name = 'Colony'
    defense = 3
    capacity = 3
    
    def __init__(self, coords, player, name, unit_num):
        super().__init__( coords, player, name, unit_num)
        self.bases = []
        self.shipyards = []
        self.shipyard_count = 0
        self.builders = 0