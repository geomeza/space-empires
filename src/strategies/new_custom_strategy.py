class NewCustomStrategy:

    def __init__(self, player_num):
        self.player_num = player_num

    def decide_ship_movement(self, ship_index, game_state):
        return (-1,0)

    def decide_purchases(self, game_state):
        return {'units' : [] , 'technology': []}

    def decide_removals(self, player_state):
        return -1
        
    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        for unit in combat_state[tuple(location)]:
            if unit['player_index'] != combat_state[tuple(location)][attacker_index]['player_index']:
                return combat_state[tuple(location)].index(unit)

    def will_colonize_planet(self, coords, game_state):
        return False

    def decide_which_units_to_screen(self, combat_state):
        return []

    def directional_input(self, current, goal):
        directions = [[1, 0],[-1, 0],[0, 1],[0, -1]]
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