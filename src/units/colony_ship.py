from units.unit import Unit 

class ColonyShip(Unit):
    cost = 8
    strength = 0          
    defense = 0
    name = 'Colonyship'
    abbr = 'CO'
    tactics = 0
    armor = 0
    class_type = 'Z'
    hull_size = 1
    maint = None
    can_atk = False
    instant_ko = True
    ship_size_needed = 1
    movement = 1