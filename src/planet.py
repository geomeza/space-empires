class Planet:
    def __init__(self, coords, colonized = False, colony = None):
        self.coords = coords
        self.colonized = colonized
        self.colony = colony

    def colonize(self, player, colony):
        self.colonized = True
        self.colony = colony

    def destroy(self):
        self.colonized = False
        self.colony = None