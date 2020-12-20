from units.unit import Unit 

class Colony(Unit):
    strength = 0
    name = 'Colony'
    class_num = 0
    defense = 1
    armor = 3
    capacity = 3
    moveable = False
    maint = None
    can_atk = False
    
    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created, colony_type = 'Normal'):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.base = None
        self.shipyards = []
        self.builders = 0
        self.colony_type = colony_type
        self.defense += tech_lvls['def']
        if colony_type == 'Home':
            self.capacity = 20

    def hit(self):
        if self.armor > 0:
            self.armor -= 1
            self.capacity -= 1
        else:
            self.destroy()

    def set_builders(self):
        for shipyard in self.shipyards:
            self.builders += shipyard.build_capacity