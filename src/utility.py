class Utility:

    def __init__(self, exist, game):
        self.exist = exist
        self.game = game
        self.tech_info = {'atk': {'lvls' : [-1,0,1,2], 'prices' : [20, 50 , 90], 'max' : 4}, 'def': {'lvls' : [-1,0,1,2], 'prices' : [20, 50 , 90], 'max' : 4}, 'move': {'lvls': [0,1,2,3,4,5], 'prices': [20, 50, 90, 130, 170], 'max' : 6}, 'shpyrd': {'lvls' : [0.5, 1.0, 1.5], 'prices' : [20, 50], 'max' : 2.0}, 'ss' : {'lvls': [0,1,2,3,4,5], 'prices' : [10,15,20,25,30], 'max' : 6}}

    def buy_tech(self, tech_type, player):
        adjuster = 1
        if tech_type == 'shpyrd':
            adjuster = 0.5
        if player.tech_lvls[tech_type] < self.tech_info[tech_type]['max']:
            current_player_lvl = self.tech_info[tech_type]['lvls'].index(player.tech_lvls[tech_type] - adjuster)
            cost = self.tech_info[tech_type]['prices'][current_player_lvl]
            if player.cp >= cost:
                player.pay(cost)
                player.tech_lvls[tech_type] = self.tech_info[tech_type]['lvls'][current_player_lvl + 1] + adjuster
                if self.game.logging:
                    print('---------')
                    print('Player', player.player_num,'Payed For:')
                    print('Level:', player.tech_lvls[tech_type],' Of', tech_type,'Technology')
                    print('---------')
        else:
            if self.game.logging:
                print(tech_type,'TECHNOLOGY MAXED OUT')
        player.update_shipyards()

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
