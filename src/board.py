from board_space import BoardSpace
from planet import Planet
import random


class Board:

    def __init__(self, size, game, planets):
        self.size = size
        self.game = game
        self.planets = []
        self.grid = dict()
        self.initialize(planets=planets)

    def initialize(self, planets):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.grid.update({(x, y): BoardSpace([x, y])})
        self.generate_planets(planets=planets)

    def update(self, players):
        all_units = []
        for player in players:
            for unit in player.units:
                all_units.append(unit)
        for space in self.grid.values():
            space.units = []
            for unit in all_units:
                if unit.coords == space.coords:
                    space.units.append(unit)

    def generate_planets(self, planets):
        if isinstance(planets, list):
            for coords in planets:
                new_planet = Planet(coords)
                self.planets.append(new_planet)
                self.grid[tuple(coords)].planet = new_planet
        elif isinstance(planets, int):
            player_coords = [
                player.home_coords for player in self.game.players]
            for i in range(planets):
                random_coords = None
                planet_coords = [planet.coords for planet in self.planets]
                while True:
                    random_coords = self.generate_coordinates()
                    if random_coords not in player_coords and random_coords not in planet_coords:
                        break
                new_planet = Planet(random_coords)
                self.planets.append(new_planet)
                self.grid[tuple(random_coords)].planet = new_planet

    def generate_coordinates(self):
        x_coord = random.randint(0, self.size[0] - 1)
        y_coord = random.randint(0, self.size[1] - 1)
        return [x_coord, y_coord]

    def get_all_units_and_coords(self):
        self.update(self.game.players)
        board = {}
        for coords, board_space in self.grid.items():
            if len(board_space.units) >= 2:
                board.update({coords: board_space.units})
        return board
