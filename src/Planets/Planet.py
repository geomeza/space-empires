class Planet():
    def __init__(self, coords, player = False):
        self.colonized = False
        self.coords = coords
        self.player = player
        self.colony = None