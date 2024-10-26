class Enemy():
    def __init__(self, velocity, x, y, aggression):
        print('shimmy yeah shimmy yeah shimmy yah')
        self.velocity = velocity
        self.x = x
        self.y = y
        self.aggression = aggression
        self.noticed = False


   

    def noticed_player(self, grid, player_location, player_direction):
        wall_present = False
        if(self.x == player_location[0]): #if enemy and player on same row
            if(self.x - player_location[0] < 0): #monster is to the left of the player
                for i in range(self.x - player_location[0]):
                    if(grid[i][self.y] == '#'):
                        wall_present = True




        self.noticed = True
        return self.noticed

        

    
    
