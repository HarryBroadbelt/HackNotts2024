import pygame
import math as maths
def distFinder((soundLoc: (int,int), playerLoc: (int,int)) -> int:
	dist = maths.sqrt((soundLoc[0]-playerLoc[0])**2 + (soundLoc[1]-playerLoc[1])**2)
	return dist