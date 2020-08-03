from game import Game

g = Game(players = 4, player_coords = [[0,0],[6,6],[0,6],[6,0]], grid_size = [13, 13], max_turns = 750,planets = 16, player_type = 'Random')
g.start()
g.complete_many_turns(5)
g.run_to_completion()
g.winner()