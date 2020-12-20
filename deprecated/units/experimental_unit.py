class ExperimentalUnit:

    def __init__(self, coords, unit_num, player, tech_lvls, game):
        self.coords = coords
        self.unit_num = unit_num
        self.player = player
        self.tech_lvls = tech_lvls
        self.alive = True
        self.game = game
        self.maintenance = 0
        self.route = None

    def destroy(self):
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)

    def move(self, direction, grid_size):
        if self.route is not None:
            direction = self.route[0]
            del self.route[0]
        test_x = self.coords[0] + direction[0]
        test_y = self.coords[1] + direction[1]
        if test_x < 0 or test_x > grid_size[0] - 1:
            if self.game.logging:
                print('Unit Reached Edge of Game Board')
                return
        if test_y < 0 or test_y > grid_size[1] - 1:
            if self.game.logging:
                print('Unit Reached Edge of Game Board')
                return
        self.coords = [test_x, test_y]

    def hit(self):
        if self.defense > 0:
            self.defense -= 1
        else:
            self.destroy()