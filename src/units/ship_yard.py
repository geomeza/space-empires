from units.unit import Unit 

class ShipYard(Unit):
    class_type = 'C'
    class_num = 3
    strength = 3
    defense = 0
    armor = 1
    cost = 6
    name = 'Shipyard'
    abbr = 'SY'
    build_size = 0
    build_capacity = 1
    hull_size = 0
    maint = None
    moveable = False
    
    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.colony = self.find_colony()
        self.colony.shipyards.append(self)

    def find_colony(self):
        found = None
        for unit in self.player.units:
            if unit.name == 'Colony':
                if unit.coords == self.coords:
                    found = unit
                    return unit
