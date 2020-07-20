import random

class Unit():
    def __init__(self, coords, player, name, unit_num):
        self.coords = coords
        self.alive = True
        self.player = player
        self.name = name
        self.defense_tech_lvl = 0
        self.attack_tech_lvl = 0
        self.unit_num = unit_num
        self.maint = 0

    def destroy(self):
        self.alive = False
        self.player.destroy_unit(self)

    def move(self,grid_size, only_direction = None):
        if only_direction is None:
            coords_changer = random.choice([[0,1],[0,-1],[1,0],[-1,0],[0,0]])
        else:
            coords_changer = random.choice([only_direction])
        coords_changer_x = coords_changer[0]
        coords_changer_y = coords_changer[1]
        test_x = self.coords[0] + coords_changer_x
        test_y = self.coords[1] + coords_changer_y
        if test_x < 0 or test_x > grid_size[0] - 1:
            if len([only_direction]) == 1:
                return [self.coords[0],self.coords[1]]
            else:
                return self.move(grid_size,only_direction = only_direction)
        if test_y < 0 or test_y > grid_size[1] - 1:
            if len(coords_changer) == 1:
                return [self.coords[0],self.coords[1]]
            else:
                return self.move(grid_size,only_direction = only_direction)
        self.coords = [test_x, test_y]

    def show_coords(self):
        print(self.name, ':', self.coords)
    
    def hit(self):
        if self.defense > 0:
            self.defense -= 1
        else:
            self.destroy()