class LevelOneBerserkerStrategy:

    def __init__(self, player_num):
        self.player_index = player_num
        self.name = 'berserk'

    def decide_ship_movement(self, ship_index, game_state):
        ship_coords = game_state['players'][self.player_index]['units'][ship_index]['coords']
        opponent_home_coords = game_state['players'][1-self.player_index]['home_coords']
        route = self.fastest_route(ship_coords, opponent_home_coords)
        if len(route) > 0:
            return tuple(route[0])
        else:
            return (0,0)

    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        for unit in combat_state[tuple(location)]:
            if unit['player'] != combat_state[tuple(location)][attacker_index]['player']:
                return combat_state[tuple(location)].index(unit)

    def directional_input(self, current, goal):
        directions = [[1, 0],[-1, 0],[0, 1],[0, -1],[0,0]]
        distances = []
        for i in range(len(directions)):
            new_loc = [current[0] + directions[i][0], current[1] + directions[i][1]]
            dist = self.distance(new_loc, goal)
            distances.append(dist)
        closest = min(distances)
        index = distances.index(closest)
        return directions[index]

    def distance(self, current, goal):
        return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**(0.5)

    def fastest_route(self, current, goal):
        route = []
        while(current != goal):
            direc = self.directional_input(current, goal)
            route.append(direc)
            current  = [current[0] + direc[0], current[1] + direc[1]]
        return route