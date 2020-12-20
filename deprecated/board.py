from units.unit import Unit 
from units.dreadnaught import Dreadnaught 
from units.scout import Scout 
from units.battlecruiser import Battlecruiser 
from units.battleship import Battleship 
from units.colony import Colony 
from units.colonyship import Colonyship 
from units.cruiser import Cruiser 
from units.destroyer import Destroyer 
from units.shipyard import Shipyard 
from board_space import BoardSpace
from planets.planet import Planet
import random

class Board:

    def __init__(self, size):
        self.dimensions = size
        self.planets = []
        self.grid = dict()

    def occupy(self, units):
        all_occupants = []
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                occupants = []
                for unit in units:
                    if unit.coords == [x,y]:
                        occupants.append(unit)
                all_occupants.append(occupants)
        return all_occupants

    def generate(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.grid.update({(x,y): BoardSpace([x,y])})
    
    def information_on_space(self,coords):
        coord = tuple(coords)
        space = self.grid[coord]
        if len(space.units) > 0:
            for unit in space.units:
                print('Player',unit.player.player_num,':',unit.name,'at',unit.coords)
        else:
            print('No Units On Space')

    def update_self(self,units):
        for space in self.grid.values():
            space.units = []
            for unit in units:
                if unit.coords == space.coords:
                    space.units.append(unit)

    def generate_coordinates(self):
        x_coord = random.randint(0,self.dimensions[0] - 1)
        y_coord = random.randint(0,self.dimensions[1] - 1)
        return [x_coord,y_coord]

    def generate_planets(self,player_coords,num_planets):
        planet_coords = []
        coords = self.generate_coordinates()
        for k in range(num_planets):
            while True:
                coords = self.generate_coordinates()
                if coords not in planet_coords and coords not in player_coords:
                    break
            planet_coords.append(coords)
            self.grid[tuple(coords)].planet = Planet(coords)
            self.planets.append(self.grid[tuple(coords)].planet)
        for coord in player_coords:
            self.grid[tuple(coords)].planet = Planet(coords)
            self.planets.append(self.grid[tuple(coords)].planet)
