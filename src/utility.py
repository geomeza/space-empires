class Utility:

    def __init__(self, exist, game):
        self.exist = exist
        self.game = game
        self.tech_info = {'atk': {'lvls': [-1, 0, 1, 2], 'prices': [20, 30, 40], 'max': 4},
                          'def': {'lvls': [-1, 0, 1, 2], 'prices': [20, 30, 40], 'max': 4},
                          'move': {'lvls': [0, 1, 2, 3, 4, 5], 'prices': [20, 30, 40, 40, 40], 'max': 6},
                          'shpyrd': {'lvls': [0, 1, 2], 'prices': [20, 30], 'max': 3},
                          'ss': {'lvls': [0, 1, 2, 3, 4, 5], 'prices': [10, 15, 20, 25, 30], 'max': 6}}

        self.ship_size_dict = {'1': 1.0, '2': 1.5, '3': 2.0}

    def buy_tech(self, tech_type, player):
        adjuster = 1
        if player.tech_lvls[tech_type] < self.tech_info[tech_type]['max']:
            current_player_lvl = self.tech_info[tech_type]['lvls'].index(
                player.tech_lvls[tech_type] - adjuster)
            cost = self.tech_info[tech_type]['prices'][current_player_lvl]
            if player.cp >= cost:
                player.pay(cost)
                new_lvl = self.tech_info[tech_type]['lvls'][current_player_lvl + 1] + adjuster
                player.tech_lvls[tech_type] = new_lvl
                if tech_type == 'shpyrd':
                    player.update_shipyards()
                if self.game.logging:
                    print('---------')
                    print('Player', player.player_num, 'Payed For:')
                    print(
                        'Level:', player.tech_lvls[tech_type], ' Of', tech_type, 'Technology')
                    print('---------')
            else:
                if self.game.logging:
                    print('---------')
                    print('Player', player.player_num, 'could not afford:')
                    print(
                        'Level:', player.tech_lvls[tech_type] + 1, ' Of', tech_type, 'Technology')
                    print('---------')
        else:
            if self.game.logging:
                print(tech_type, 'TECHNOLOGY MAXED OUT')

    def directional_input(self, current, goal):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1,1], [-1,1]]
        distances = []
        for i in range(len(directions)):
            new_loc = [current[0] + directions[i]
                       [0], current[1] + directions[i][1]]
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
            current = [current[0] + direc[0], current[1] + direc[1]]
        return route
