class Planet:
    def __init__(self, coords, player = None):
        self.coords = coords
        self.colonized = False
        self.player = player
        self.colony = None
        self.colony_type = 'Normal'