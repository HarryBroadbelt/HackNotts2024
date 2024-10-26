import pygame
import math as maths
import typing
from enum import Enum

class Direction(Enum):
    """Relative to north"""
    LEFT = 1
    RIGHT = 2
    FORWARD = 3
    BACKWARD = 4

def distFinder(soundLoc: (int,int), playerLoc: (int,int)) -> int:
    dist = maths.sqrt((soundLoc[0]-playerLoc[0])**2 + (soundLoc[1]-playerLoc[1])**2)
    return dist

def soundVolume(distance: float, primaryDir: Direction, muffling: int) -> (int,int):
    """Use this with "set_volume()"."""
    if primaryDir.value == 1:
        voL = 2/(distance+muffling)
        voR = 1/(distance+muffling)
    elif primaryDir.value == 2:
        voL = 1/(distance+muffling)
        voR = 2/(distance+muffling)
    else:
        voL = voR = 1.5/(distance+muffling)
    return (voL, voR)

def checkWalls(grid,soundLoc,playerLoc):
    muffling = 0
    if abs(soundLoc[0]-playerLoc[0]) > abs(soundLoc[1]-playerLoc[1]):
        if soundLoc[0]-playerLoc[0] < 0:
            if grid[soundLoc[0]+1][soundLoc[1]] == "#":
                muffling += 1
        else:
            if grid[soundLoc[0]-1][soundLoc[1]] == "#":
                muffling += 1
    else:
        if soundLoc[1]-playerLoc[1] < 0:
            if grid[soundLoc[0]][soundLoc[1]+1] == "#":
                muffling += 1
        else:
            if grid[soundLoc[0]][soundLoc[1]-1] == "#":
                muffling += 1
        

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
    
