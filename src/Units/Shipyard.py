from Units.Unit import Unit 

class Shipyard(Unit):
    class_type = 'C'
    class_num = 3
    strength = 3
    defense = 0
    speed = 0
    armor=1
    cost=6
    name = 'Shipyard'
    abbr = 'SY'
    build_capacity = 1
    
    def __init__(self, coords, player, name, unit_num, colony):
        super().__init__( coords, player, name, unit_num)
        self.colony = colony
