class Unit:
    moveable = True
    can_atk = True
    instant_ko = False
    brought_into_fight = False

    def __init__(self, coords, unit_num, player, tech_lvls, game, turn_created):
        self.coords = coords
        self.unit_num = unit_num
        self.player = player
        self.tech_lvls = tech_lvls
        self.alive = True
        self.game = game
        self.maint = 0
        self.route = None
        self.turn_created = turn_created

    def destroy(self):
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)

    def move(self, direction, grid_size):
        if self.route is not None:
            if len(self.route) > 0:
                direction = self.route[0]
                del self.route[0]
            else:
                direction = [0,0]
        directions = [[1, 0],[-1, 0],[0, 1],[0, -1],[0,0]]
        test_x = self.coords[0] + direction[0]
        test_y = self.coords[1] + direction[1]
        distance = round(self.game.utility.distance(self.coords, [test_x, test_y]),3)
        if direction not in directions:
            if self.game.invalidation:
                if self.game.logging:
                    print('Player made invalid move')
                self.player.self_destruct()
            return
        if test_x < 0 or test_x > grid_size[0] - 1:
            if self.game.invalidation:
                if self.game.logging:
                    print('Player made invalid move')
                self.player.self_destruct()
            return
        if test_y < 0 or test_y > grid_size[1] - 1:
            if self.game.invalidation:
                print('NAHHHH BRUHHHH', direction, [test_x,test_y], self.coords)
                if self.game.logging:
                    print('Player made invalid move')
                self.player.self_destruct()
            return
        self.coords = [test_x, test_y]

    def hit(self):
        if self.armor > 1:
            self.armor -= 1
        else:
            self.destroy()

    def set_route(self, goal):
        self.route = self.game.utility.fastest_route(self.coords, goal)