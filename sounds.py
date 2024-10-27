import pygame
import math as maths
import typing
from enum import Enum

class Direction(Enum):
    """Relative to north"""
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "U"
    BACKWARD = "D"

def distFinder(soundLoc: (int,int), playerLoc: (int,int)) -> float:
    dist = maths.sqrt((soundLoc[0]-playerLoc[0])**2 + (soundLoc[1]-playerLoc[1])**2)
    return dist

def soundVolume(distance: float, primaryDir: Direction, muffling: int) -> (int,int):
    """Use this with "set_volume()"."""
    if primaryDir.value == "L":
        voL = 2/(distance+muffling)
        voR = 1/(distance+muffling)
    elif primaryDir.value == "R":
        voL = 1/(distance+muffling)
        voR = 2/(distance+muffling)
    else:
        voL = voR = 1.5/(distance+muffling)
    return (voL, voR)

def checkWalls(grid,soundLoc,playerLoc):
    muffling = 0
    atPlayer = False
    while not atPlayer:
        if abs(soundLoc[0]-playerLoc[0]) > abs(soundLoc[1]-playerLoc[1]):
            if soundLoc[0]-playerLoc[0] < 0:
                if grid[soundLoc[0]+1][soundLoc[1]] == "#":
                    muffling += 1
                soundLoc[0]+=1
            else:
                if grid[soundLoc[0]-1][soundLoc[1]] == "#":
                    muffling += 1
                soundLoc[0]-=1
        elif abs(soundLoc[0]-playerLoc[0]) < abs(soundLoc[1]-playerLoc[1]):
            if soundLoc[1]-playerLoc[1] < 0:
                if grid[soundLoc[0]][soundLoc[1]+1] == "#":
                    muffling += 1
                soundLoc[1]+=1
            else:
                if grid[soundLoc[0]][soundLoc[1]-1] == "#":
                    muffling += 1
                soundLoc[1]-=1
        else:
            atPlayer = True
    return muffling
        
        

def findSoundDirection(playerLoc: (int,int), playerDirection: Direction, soundLoc: (int, int)) -> Direction:
    xDif = soundLoc[0] - playerLoc[0]
    yDif = soundLoc[1] - playerLoc[1]

    if playerDirection == Direction.FORWARD:
        if xDif < 0:
            return Direction.LEFT
        elif xDif > 0:
            return Direction.RIGHT
        elif yDif >= 0:
            return Direction.FORWARD
        else:
            return Direction.BACKWARD
    elif playerDirection == Direction.BACKWARD:
        if xDif < 0:
            return Direction.RIGHT
        elif xDif > 0:
            return Direction.LEFT
        elif yDif >= 0:
            return Direction.BACKWARD
        else:
            return Direction.FORWARD
    elif playerDirection == Direction.LEFT:
        if yDif < 0:
            return Direction.LEFT
        elif yDif > 0:
            return Direction.RIGHT
        elif xDif >= 0:
            return Direction.FORWARD
        else:
            return Direction.BACKWARD
    else:
        if yDif < 0:
            return Direction.RIGHT
        elif yDif > 0:
            return Direction.LEFT
        elif xDif >= 0:
            return Direction.BACKWARD
        else:
            return Direction.FORWARD
    
