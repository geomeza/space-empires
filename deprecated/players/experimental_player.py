class ExperimentalPlayer:

    def __init__(self, strategy, player_num, starting_coords, game):
        self.strategy = strategy
        self.player_num = player_num
        self.tech_lvls = {'atk' : 0, 'def' : 0, 'move' : 1, 'shpyrd' : 1, 'ss' : 1}
        self.home_coords = starting_coords
        self.game = game
        self.units = []
        self.cp = 0
    
    def build_unit(self, unit_name, coords, pay = True):
        new_unit = unit_name(coords, len(self.units) + 1, self, [0], self.game)
        if pay:
            self.cp -= new_unit.maint
        self.units.append(new_unit)

    def make_colony(self, colony_ship, coords, col_type = 'Normal'):
        if col_type == 'Home':
            home_colony = Colony()
        else:
            new_colony = 

    # def buy_tech