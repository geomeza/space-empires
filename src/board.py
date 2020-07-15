from Units.Unit import Unit 
from Units.Dreadnaught import Dreadnaught 
from Units.Scout import Scout 
from Units.Battlecruiser import Battlecruiser 
from Units.Battleship import Battleship 
from Units.Colony import Colony 
from Units.Colonyship import Colonyship 
from Units.Cruiser import Cruiser 
from Units.Destroyer import Destroyer 
from Units.Shipyard import Shipyard 
from Planets.Planet import Planet 
from Game import Game
from Player import Player

class Board():

	def __init__(self, size):
		self.dimensions = size

	def occupy(self, units):
		all_occupants = []
		for x in range(self.dimensions[0]):
			for y in range(self.dimensions[1]):
				occupants = []
				for unit in units:
					if unit.coords == [x,y]:
						occupants.append(unit)
				all_occupants.append(occupants)

