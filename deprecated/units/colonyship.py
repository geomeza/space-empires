def distance(current, goal):
    return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**(0.5)

from units.unit import Unit 

class Colonyship(Unit):
    cost = 8
    strength = 0          
    defense = 0
    speed = 1
    name = 'Colony Ship'
    abbr = 'CO'
    class_num = 0
    armor = 0
    class_type = 'Z'
    hull_size = 1

    # def find_closest_planet(self):