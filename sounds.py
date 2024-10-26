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

def soundVolume(distance: int, primaryDir: Direction) -> (int,int):
    """Use this with "set_volume()"."""
    if primaryDir.value == 1:
        voL = 2/distance
        voR = 1/distance
    elif primaryDir.value == 2:
        voL = 1/distance
        voR = 2/distance
    else:
        voL = voR = 1.5/distance
    return (voL, voR)

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
    
