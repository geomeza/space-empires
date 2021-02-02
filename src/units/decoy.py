from units.unit import Unit 

class Decoy(Unit):
    cost = 1
    strength = 0          
    defense = 0
    name = 'Decoy'
    abbr = 'DY'
    class_num = 0
    armor = 0
    class_type = 'Z'
    hull_size = 0
    maint = None
    can_atk = False
    instant_ko = True
    ship_size_needed = 1
    movement = 1