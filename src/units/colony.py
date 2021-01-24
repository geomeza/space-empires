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
    ship_size_needed = 0
    
    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created, colony_type = 'Normal'):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.capacity_dict = {'Normal': [1,2], 'Home': [10,15]}
        self.base = None
        self.shipyards = []
        self.builders = 0
        self.colony_type = colony_type
        self.defense += tech_lvls['def']
        if colony_type == 'Home':
            self.capacity = 20

    def hit(self):
        if self.armor > 1:
            self.armor -= 1
            self.capacity = self.capacity_dict[self.colony_type][self.armor-1]
            print('Capacity', self.capacity)
        else:
            self.destroy()

    def destroy(self):
        planet = self.player.find_planet(self.coords)
        planet.destroy()
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)

    def set_builders(self):
        self.builders = 0
        for shipyard in self.shipyards:
            self.builders += shipyard.build_capacity