from Game import Game

g = Game(players = 4, player_coords = [[0,0],[4,4],[0,4],[4,0]], combat_points = 50, grid_size = [5, 5], max_turns = 250)
g.start()
g.complete_many_turns(25)
g.run_to_completion()
g.winner()

# P_T = Player(50, 1)
# P_T.generate_units([5,5])
# print([unit.name for unit in P_T.units])
# P_T.com_points += 50
# P_T.units.remove(P_T.units[0])
# P_T.units.remove(P_T.units[1])
# P_T.generate_units([5,5])
# print([unit.name for unit in P_T.units])
# Dreadnaught([5,5],P_T,'Dreadnaught')
# print(P_T.units[1].strength)
# P_T.units[1].strength += 12
# print(P_T.units[1].strength)


# print(Dreadnaught.speed)
# Testunit = Dreadnaught([5,5],P_T,'Dreadnaught',4)
# Testunit.speed += 20
# print(Dreadnaught.speed, Testunit.speed)