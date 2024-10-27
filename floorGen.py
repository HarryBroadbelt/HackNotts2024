import random
import math as maths
import heapq

class Node:
    def __init__(self):
        self.f = float("inf")
        self.q = float("inf")
        self.h = 0
        self.parent = (0,0)

def isDest(row,col,floor):
    return row == floor.exit[0] and col == floor.exit[1]

def calcHeuristic(row, col, floor):
    return((row-floor.exit[0])**2+(col-floor.exit[1])**2)

def isValid(row,col):
    return (row>=0) and (row<30) and (col>=0) and (col<30)

def unblocked(grid,row,col,floor):
    return grid[row][col] == " " or (row,col) == floor.exit

def tracePath(nodeDetails, floor):
    path = []
    row = floor.exit[0]
    col = floor.exit[1]
    while not(nodeDetails[row][col].parent == (row,col)):
        path.append((row,col))
        tNode = nodeDetails[row][col].parent
        row = tNode[0]
        col = tNode[1]
        path.append((row,col))
        path.reverse()
    print(path)

def aStarAlgo(start,end,floor):
    
    closedList = [[False for _ in range(30)] for _ in range(30)]
    nodeDetails = [[Node() for _ in range(30)] for _ in range(30)]
    nodeDetails[start[0]][start[1]].f = 0
    nodeDetails[start[0]][start[1]].g = 0
    nodeDetails[start[0]][start[1]].h = 0
    nodeDetails[start[0]][start[1]].parent = start
    openList = []
    heapq.heappush(openList, ((0.0), start[0], start[1]))
    foundDest = False
    while len(openList) > 0:
        p = heapq.heappop(openList)
        i = p[1]
        j = p[2]
        closedList[i][j] = True
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,-1)]
        for dir in directions:
            newI = i + dir[0]
            newJ = j+dir[1]
            if isValid(newI,newJ) and unblocked(floor.grid,newI,newJ, floor) and not closedList[newI][newJ]:
                if isDest(newI, newJ, floor):
                    nodeDetails[newI][newJ].parent=(i,j)
                    #print("found path")
                    #tracePath(nodeDetails, floor)
                    foundDest=True #found path
                    return True
                else:
                    gNew = nodeDetails[i][j].g+1.0
                    hNew=calcHeuristic(newI,newJ,floor)
                    fNew=gNew+hNew
                    if nodeDetails[newI][newJ].f==float("inf") or nodeDetails[newI][newJ].f>fNew:
                        heapq.heappush(openList,(fNew,newI,newJ))
                        nodeDetails[newI][newJ].f=fNew
                        nodeDetails[newI][newJ].g=gNew
                        nodeDetails[newI][newJ].h=hNew
                        nodeDetails[newI][newJ].parent=(i,j)
    return False

def findExit(floor,i,u):
    if floor.grid[i][u] == "#":
        """
        for offset in range(-1,2): 
            surroundingWalls = 0
            try:
                if floor.grid[i+offset][u] == "#":
                    surroundingWalls += 1
            except IndexError:
                pass
            try:
                if floor.grid[i][u+offset] == "#":
                    surroundingWalls += 1
            except IndexError:
                pass
        if surroundingWalls == 5:
            floor.exit = [i,u]
            return True
        """
        for offset in range(-1,2):
            try:
                if floor.grid[i+offset][u] == " ":
                    floor.exit = (i,u)
                    return True
            except IndexError:
                pass
            try:
                if floor.grid[i][u+offset] == " ":
                    floor.exit = (i,u)
                    return True
            except IndexError:
                pass
        """
        try:
            if floor.grid[i+1][u] == " " or floor.grid[i-1][u] == " " or floor.grid[i][u+1] == " " or floor.grid[i][u-1] == " ":
                floor.exit = (i,u)
        except IndexError:
            print(i,u)
            pass
        """
    return False


class Floor:
    def __init__(self):

        exitFound = False
        playerPlaced = False
        monsterPlaced = False
        aStarPassed = False
            
        while not exitFound or not playerPlaced or not monsterPlaced or not aStarPassed:
            MAX_SIZE = 20
            MAX_TUNNELS = 60
            MAX_LENGTH = 8
            self.exit = [1, 0]
            self.playerSpawn = [0,1]
            self.monsterSpawn = [0,0]
            exitFound = False
            playerPlaced = False
            monsterPlaced = False
            aStarPassed = False
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
            randI = random.randint(1,MAX_SIZE)
            randU = random.randint(1,MAX_SIZE)
            for i in range(randI,MAX_SIZE):
                for u in range(randU,MAX_SIZE):
                    if not exitFound:
                        exitFound = findExit(self,i,u)
                        print(exitFound)
                    if self.grid[i][u] == " ":
                        try:
                            if self.grid[i][u+1] == " " or self.grid[i][u-1] == " ":
                                if self.grid[i+2][u] == " ":
                                    if self.grid[i+1][u+1] == "#" and self.grid[i+1][u-1] == "#":
                                        self.grid[i+1][u] = " "
                                elif self.grid[i-2][u] == " ":
                                    if self.grid[i-1][u+1] == "#" and self.grid[i-1][u-1] == "#":
                                        self.grid[i-1][u] = " "
                        except IndexError:
                            pass
                        try:
                            if self.grid[i+1][u] == " " or self.grid[i-1][u] == " ":
                                if self.grid[i][u+2] == " ":
                                    if random.randint(0,100) > 25 and self.grid[i+1][u+1] == "#" and self.grid[i-1][u+1] == "#":
                                        self.grid[i][u+1] = " "
                                elif self.grid[i][u-2] == " ":
                                    if random.randint(0,100) > 25 and self.grid[i+1][u-1] == "#" and self.grid[i-1][u-1] == "#":
                                        self.grid[i][u-1] = " "
                        except IndexError:
                            pass
                    if exitFound and self.grid[i][u] == " " and not playerPlaced:
                        if maths.sqrt((i-self.exit[0])**2+(u-self.exit[1])**2) >= 6:
                            self.playerSpawn = [i,u]
                            playerPlaced = True

                
            for i in range(1,randI):
                for u in range(1,randU):
                    if not exitFound:
                        exitFound = findExit(self,i,u)
                        print(exitFound)
                    if self.grid[i][u] == " ":
                        try:
                            if self.grid[i][u+1] == " " or self.grid[i][u-1] == " ":
                                if self.grid[i+2][u] == " ":
                                    if random.randint(0,100) > 25 and self.grid[i+1][u+1] == "#" and self.grid[i+1][u-1] == "#":
                                        self.grid[i+1][u] = " "
                                elif self.grid[i-2][u] == " ":
                                    if random.randint(0,100) > 25 and self.grid[i-1][u+1] == "#" and self.grid[i-1][u-1] == "#":
                                        self.grid[i-1][u] = " "
                        except IndexError:
                            pass
                        try:
                            if self.grid[i+1][u] == " " or self.grid[i-1][u] == " ":
                                if self.grid[i][u+2] == " ":
                                    if random.randint(0,100) > 25 and self.grid[i+1][u+1] == "#" and self.grid[i-1][u+1] == "#":
                                        self.grid[i][u+1] = " "
                                elif self.grid[i][u-2] == " ":
                                    if random.randint(0,100) > 25 and self.grid[i+1][u-1] == "#" and self.grid[i-1][u-1] == "#":
                                        self.grid[i][u-1] = " "
                        except IndexError:
                            pass
                    if exitFound and self.grid[i][u] == " " and not playerPlaced:
                        if maths.sqrt((i-self.exit[0])**2+(u-self.exit[1])**2) >= 12:
                            self.playerSpawn = [i,u]
                            playerPlaced = True
            crazyList = []
            for i in range(1,MAX_SIZE):
                for u in range(1,MAX_SIZE):
                    if self.grid[i][u] == " " and (i,u) != self.exit and (i,u) != self.playerSpawn and maths.sqrt((i-self.playerSpawn[0])**2+(u-self.playerSpawn[1])**2) >= 6:
                        crazyList.append((i,u))
            self.monsterSpawn = random.choice(crazyList)
            monsterPlaced = True
            playerExit = aStarAlgo(self.playerSpawn,self.exit,self)
            monsterExit = aStarAlgo(self.monsterSpawn,self.exit,self)
            aStarPassed = playerExit and monsterExit
            print(f"pEx:{playerExit}")
            print(f"mEx:{monsterExit}")

            self.exit = [self.exit[0], self.exit[1]]
                        
                            
        
        #print(self.grid)
if __name__ == "__main__":
    floor = Floor()
    for i in range(len(floor.grid)):
        print(floor.grid[i])
    print(floor.playerSpawn)
    print(floor.exit)
    print(floor.monsterSpawn)

