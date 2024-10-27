import random

"""
ENEMY TYPES:
- Chaser: Acts normal but speeds up when it sees the player
  - Could have a brief wind-up when he sees the player? eg a pause to scream before rapid acceleration to max speed. -M
- Stalker: Teleports randomly nearby the player. If the player sees them they must look away within x seconds or it starts to chase.
- Meaty Michael: Stops moving if it sees the player
- Phased: Moves randomly but can move through walls at a greatly reduced rate

"""


class Enemy():
    def __init__(self, velocity, x, y, type, art):
        self.art = art
        print('shimmy yeah shimmy yeah shimmy yah')
        #type = 'Stalker'
        if(type == 'Chaser'):
            max_aggro = 10
        elif(type == 'Stalker'):
            max_aggro = 6
        elif(type=='Meaty Michael'):
            max_aggro = 3
        elif(type=='Phased'):
            max_aggro = 6
        self.velocity=velocity
        self.x=x
        self.y=y
        self.attributes = {'min_aggro':3,'max_aggro':max_aggro}
        self.current_aggro = self.attributes['min_aggro']
        self.noticed=False
        self.type=type


    def noticed_player(self, grid, player_location, player_direction):
        self.noticed = False
        same_row = False
        wall_present=False
        if(self.y == player_location[1]): #if enemy and player on same row
            same_row = True
            if(self.x - player_location[0]<0): #enemy is to the left of the player
                for i in range(self.x, player_location[0],1): #check to see if a wall exists between the enemy and player
                    if(grid[i][self.y]=='#'):
                        wall_present=True
            else:
                for i in range(self.x, player_location[0],-1): #check to see if a wall exists between the enemy and player
                    if(grid[i][self.y]=='#'):
                        wall_present=True
        elif(self.x== player_location[0]): #if enemy and player are on same column
            same_row = True
            if(self.y-player_location[1]>0): #enemy is below the player
                for i in range(player_location[1], self.y, 1): #check to see if a wall exists between the enemy and player
                    if(grid[self.x][i]=='#'):
                        wall_present=True
            else:
                for i in range(player_location[1], self.y,-1): #check to see if a wall exists between the enemy and player
                    if(grid[self.x][i]=='#'):
                        wall_present=True
    
        if(wall_present or same_row == False):
            self.current_aggro = self.current_aggro - 1
            if(self.current_aggro < self.attributes['min_aggro']):
                self.current_aggro = self.attributes['min_aggro']
            return False
        
        self.noticed=True
        if(self.type=='Chaser'):
            self.current_aggro=self.current_aggro+3
            if(self.current_aggro>self.attributes['max_aggro']):
                self.current_aggro=self.attributes['max_aggro']
        return self.noticed
    
    def move_towards_player(self, grid, distance, player_location):
        if(self.x-player_location[0]<0 and self.y==player_location[1]):
            self.x=self.x+distance
        elif(self.x-player_location[0]>0 and self.y==player_location[1]):
            self.x=self.x-distance
        elif(self.y-player_location[1]>0 and self.x==player_location[0]):
            self.y=self.y-distance
        elif(self.y-player_location[1]<0 and self.x==player_location[0]):
            self.y=self.y+distance

        return [self.x,self.y]

    def ai_process(self, grid, player_location):
        enemy_position = [self.x, self.y]
        if(self.type == 'Phased'):
            rng = random.randint(1,8)
            while(1):
                if(rng == 1 and self.x+1 < len(grid)):
                    self.x = self.x + 1
                    self.y = self.y
                    break
                elif(rng == 2 and self.x-1 > 0):
                    self.x = self.x - 1
                    self.y = self.y
                    break
                elif(rng == 3 and self.y+1 < len(grid)):
                    self.x = self.x
                    self.y = self.y + 1
                    break
                elif(rng == 4 and self.y-1 > 0):
                    self.x = self.x
                    self.y = self.y - 1
                    break
                break
            enemy_position = [self.x, self.y]
        elif(self.type == 'Stalker'):
            #enemy_position=self.move_towards_player(grid,1,player_location)
            print('needs fixing.')
        elif(self.noticed):
            if(self.type != 'Meaty Michael'):
                enemy_position=self.move_towards_player(grid,1,player_location)
            else:
                enemy_position = [self.x, self.y]
        else:
            rng = random.randint(1,8)
            while(1):
                if(rng == 1 and grid[self.x+1][self.y] != '#'):
                    self.x = self.x + 1
                    self.y = self.y
                    break
                elif(rng == 2 and grid[self.x-1][self.y] != '#'):
                    self.x = self.x - 1
                    self.y = self.y
                    break
                elif(rng == 3 and grid[self.x][self.y+1] != '#'):
                    self.x = self.x
                    self.y = self.y + 1
                    break
                elif(rng == 4 and grid[self.x][self.y-1] != '#'):
                    self.x = self.x
                    self.y = self.y - 1
                    break
                break
            enemy_position = [self.x, self.y]
            

        return enemy_position


        

    
    
