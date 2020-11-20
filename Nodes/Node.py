import pygame
from .Vector import Vector

class Node:

    def __init__(self, X, Y, Parent = None, Start =False, Goal = False):
        self.current = Vector(X, Y)
        self.Previous = None
        if(Start):
            self.cheapest = 0
        if Parent != None:
            self.Previous = Parent

    def SetDistance(self, Target):
        self.DistanceScore = abs(Target.current.x - self.current.x) + abs(Target.current.y - self.current.y)
