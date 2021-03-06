from units.unit import Unit 

class Base(Unit):
    class_type = 'A'
    hull_size = 2
    tactics = 5
    strength = 7
    defense = 2
    armor = 3
    cost = 12
    ship_size_needed = 2
    name = 'Base'
    abbr = 'B'
    # movement = 

    moveable = False
    maint = None
    
    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        super().__init__(coords, unit_num, player, tech_lvls, game, turn_created)
        self.colony = self.find_colony()
        self.colony.base = self

    def find_colony(self):
        found = None
        for unit in self.player.units:
            if unit.name == 'Colony':
                if unit.coords == self.coords:
                    found = unit
                    return unit