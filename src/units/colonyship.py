from units.unit import Unit 

class Colonyship(Unit):
    cost = 8
    strength = 0          
    defense = 0
    name = 'Colony Ship'
    abbr = 'CO'
    class_num = 0
    armor = 0
    class_type = 'Z'
    hull_size = 1
    maint = None
    can_atk = False
    instant_ko = True
    build_size = 1