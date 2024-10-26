class Enemy():
    def __init__(self, velocity, x, y, type):
        print('shimmy yeah shimmy yeah shimmy yah')
        if(type == 'Chaser'):
            max_aggro = 10
        if(type == 'Stalker'):
            max_aggro = 6
        self.velocity=velocity
        self.x=x
        self.y=y
        self.attributes = {'min_aggro':3,'max_aggro':max_aggro}
        self.current_aggro = self.attributes['min_aggro']
        self.noticed=False
        self.type=type


    def noticed_player(self, grid, player_location, player_direction):
        wall_present=False
        print('1')
        if(self.y == player_location[1]): #if enemy and player on same row
            print('2')
            if(self.x - player_location[0]<0): #enemy is to the left of the player
                print('3')
                for i in range(self.x, player_location[0],1): #check to see if a wall exists between the enemy and player
                    if(grid[i][self.y]=='#'):
                        wall_present=True
            else:
                print('4')
                for i in range(self.x, player_location[0],-1): #check to see if a wall exists between the enemy and player
                    if(grid[i][self.y]=='#'):
                        wall_present=True
        elif(self.x== player_location[0]): #if enemy and player are on same column
            print('5')
            if(self.y-player_location[1]<0): #enemy is below the player
                print('6')
                for i in range(self.y, player_location[1], 1): #check to see if a wall exists between the enemy and player
                    if(grid[self.x][i]=='#'):
                        wall_present=True
            else:
                print('7')
                for i in range(self.y, player_location[1],-1): #check to see if a wall exists between the enemy and player
                    if(grid[self.x][i]=='#'):
                        wall_present=True

        if(wall_present):
            return False
        
        self.noticed=True
        if(self.type=='Chaser'):
            self.current_aggro=self.current_aggro+3
            if(self.current_aggro>self.attributes['max_aggro']):
                self.current_aggro=self.attributes['max_aggro']
        return self.noticed
    
    def move_towards_player(self, grid, distance, player_location):
        if(self.x-player_location[0]<0 and self.x==player_location[0]):
            self.x=self.x+distance
        elif(self.x-player_location[0]>0 and self.x==player_location[0]):
            self.x=self.x-distance
        elif(self.y-player_location[1]<0 and self.y==player_location[1]):
            self.y=self.y-distance
        elif(self.y-player_location[1]<0 and self.y==player_location[1]):
            self.y=self.y+distance

        return [self.x,self.y]

    def ai_process(self, grid, player_location):
        if(self.noticed):
            enemy_position=self.move_towards_player(grid,1,player_location)

        return enemy_position


        

    
    
