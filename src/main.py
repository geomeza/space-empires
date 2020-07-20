from Game import Game

g = Game(players = 4, player_coords = [[0,0],[11,11],[0,11],[11,0]], combat_points = 50, grid_size = [12, 12], max_turns = 500,planets = 16)
g.start()
g.complete_many_turns(25)
g.run_to_completion()
g.winner()