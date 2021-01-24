class CombatStrategy:
    def __init__(self,player_num):
        self.player_num = player_num
        self.next_buy = 'Destroyers'

    def decide_ship_movement(self,ship_index, game_state):
        if game_state['players'][self.player_num-1]["units"][ship_index]["coords"][1]>2:
             return (0,-1)
        elif game_state['players'][self.player_num-1]["units"][ship_index]["coords"][1]<2:
             return (0,1)
        else:
            return (0,0)


    def decide_purchases(self,game_state):
      return_dic = {
            'units': [],
            'technology': [] 
        }
      new_shipsize= game_state['players'][self.player_num-1]['technology']['shipsize']
      if game_state['players'][self.player_num-1]['technology']['shipsize']<2:
        new_shipsize= game_state['players'][self.player_num-1]['technology']['shipsize']+1
        return_dic['technology'].append('shipsize')
      if new_shipsize>=2:
        if self.next_buy == 'Destroyers':
          self.next_buy = 'Scout'
          return_dic['unit'].append({'type': 'Destroyer', 'coords': (2,self.player_num*4)})
        elif self.next_buy == 'Scout':
          self.next_buy = 'Destroyers'
          return_dic['unit'].append({'type': 'Scout', 'coords': (2,self.player_num*4)})
      return return_dic

    def will_colonize_planet(self, coordinates, game_state):
      return False

    def decide_removals(self, game_state):
      return game_state["player"][self.player_num]["unit"][0]["unit number"]-1#assuming unit number starts at 1#This would remove the oldest ship, however, need to make this more complicated to remove multiple ships, currently this needs to be run mutliple times and doesn't account for ships that have no cost to maintain.

    def decide_which_unit_to_attack(self,combat_state, coords, attacker_index):
      for ship in combat_state[coords]:
        if ship['player']!=self.player_num:
          return combat_state['coords'].index(ship)
          break
      

    def decide_which_units_to_screen(self, combat_state):
      player_count = 0
      enemy_count = 0
      screens = []
      # for ship in combat_state['order']:
      #   if ship['player']!=self.player_num:
      #     enemy_count=+1
      # for ship in combat_state['order']:
      #   if ship['player']==self.player_num:
      #     player_count=+1
      #     if player_count >= enemy_count:
      #       screens.append(combat_state['order'].index(ship))
      #i thought this was nice
      return screens