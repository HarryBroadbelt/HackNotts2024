import random
class Floor:

    def __init__(self):

        LV_GEN = "rand"

        self.exit = [1, 0]
        exitFound = False
        
        if LV_GEN == "rand":
            
            MAX_SIZE = 30
            MAX_TUNNELS = 50
            MAX_LENGTH = 15

            self.grid = []

            for i in range(MAX_SIZE):
                self.grid.append([])
                for j in range(MAX_SIZE):
                    self.grid[-1].append("#")

            tunnel = [random.randint(1, MAX_SIZE - 2), random.randint(1, MAX_SIZE - 2)]

            for i in range(MAX_TUNNELS):
                tunnel_dir = random.choice([[0, 1], [1, 0], [0, -1], [-1, 0]])
                self.grid[tunnel[0]][tunnel[1]] = " "
                tunnel = [tunnel[0] + tunnel_dir[0], tunnel[1] + tunnel_dir[1]]
                if tunnel[0] == 0:
                    tunnel[0] = 1
                if tunnel[0] == MAX_SIZE - 1:
                    tunnel[0] = MAX_SIZE - 2
                if tunnel[1] == 0:
                    tunnel[1] = 1
                if tunnel[1] == MAX_SIZE - 1:
                    tunnel[1] = MAX_SIZE - 2
                for j in range(random.randint(0, MAX_LENGTH)):
                    self.grid[tunnel[0]][tunnel[1]] = " "
                    if tunnel_dir == [0,1] or tunnel_dir == [0,-1]:
                        self.grid[tunnel[0]+1][tunnel[1]] = "#"
                        self.grid[tunnel[0]-1][tunnel[1]] = "#"
                    else:
                        self.grid[tunnel[0]][tunnel[1]+1] = "#"
                        self.grid[tunnel[0]][tunnel[1]-1] = "#"
                    tunnel = [tunnel[0] + tunnel_dir[0], tunnel[1] + tunnel_dir[1]]
                    if tunnel[0] == 0:
                        tunnel[0] = 1
                    if tunnel[0] == MAX_SIZE - 1:
                        tunnel[0] = MAX_SIZE - 2
                    if tunnel[1] == 0:
                        tunnel[1] = 1
                    if tunnel[1] == MAX_SIZE - 1:
                        tunnel[1] = MAX_SIZE - 2
            for i in range(1,MAX_SIZE):
                for u in range(1,MAX_SIZE):
                    if not exitFound:
                        if self.grid[i][u] == " ":
                            surroundingWalls = 0
                            for offset in range(-1,2):
                                if self.grid[i+offset][u] == "#":
                                    surroundingWalls += 1
                                if self.grid[i][u+offset] == "#":
                                    surroundingWalls += 1
                            if surroundingWalls == 3:
                                self.exit = [i,u]
                                exitFound = True
                    if self.grid[i][u] == " ":
                        try:
                            if self.grid[i][u+1] == " " or self.grid[i][u-1] == " ":
                                if self.grid[i+2][u] == " ":
                                    if random.randint(0,100) > 75 and self.grid[i+1][u+1] == "#" and self.grid[i+1][u-1] == "#":
                                        self.grid[i+1][u] = " "
                                elif self.grid[i-2][u] == " ":
                                    if random.randint(0,100) > 75 and self.grid[i-1][u+1] == "#" and self.grid[i-1][u-1] == "#":
                                        self.grid[i-1][u] = " "
                        except IndexError:
                            pass
                        try:
                            if self.grid[i+1][u] == " " or self.grid[i-1][u] == " ":
                                if self.grid[i][u+2] == " ":
                                    if self.grid[i+1][u+1] == "#" and self.grid[i-1][u+1] == "#":
                                        self.grid[i][u+1] = " "
                                elif self.grid[i][u-2] == " ":
                                    if self.grid[i+1][u-1] == "#" and self.grid[i-1][u-1] == "#":
                                        self.grid[i][u-1] = " "
                        except IndexError:
                            pass
                        
        for i in range(len(self.grid)):
            print(self.grid[i])
        #print(self.grid)
floor = Floor()
