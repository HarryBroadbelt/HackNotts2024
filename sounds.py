import pygame
import math as maths
import typing
from enum import Enum

class direction(Enum):
    LEFT = 1
    RIGHT = 2
    FRONT = 3
    BACK = 4

def distFinder(soundLoc: (int,int), playerLoc: (int,int)) -> int:
    dist = maths.sqrt((soundLoc[0]-playerLoc[0])**2 + (soundLoc[1]-playerLoc[1])**2)
    return dist

def soundVolume(distance: int, primaryDir: direction) -> (int,int):
    """Use this with "set_volume()"."""
    if primaryDir == 1:
        voL = 2/distance
        voR = 1/distance
    elif primaryDir == 2:
        voL = 1/distance
        voR = 2/distance
    else:
        voL = voR = 1.5/distance
    return (voL, voR)
