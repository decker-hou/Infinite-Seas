import pygame, math
from gameSprite import GameSprite
from Utils import Utils

class MovingSprite(GameSprite):
    def __init__(self, data, x, y, img, v, a, deaccel=None):
        super().__init__(data, x, y, img)
        self.v = v
        self.targetV = v
        self.accel = a
        self.deaccel = a if (deaccel == None) else deaccel
        self.angle = 0
        self.direction = 1

        self.targetX = self.x
        self.targetY = self.y

    def flipSprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def turn(self):
        self.direction *= -1
        self.flipSprite()

    def doTurn(self, targetX):
        if ( (targetX > self.x and self.direction == -1) or
             (targetX < self.x and self.direction == 1) ):
            self.turn()

    def setTarget(self, x, y):
        self.targetX = x
        self.targetY = y
        self.doTurn(x)

    def move(self):
        self.x += self.v * math.cos(self.angle)
        self.y -= self.v * math.sin(self.angle)

    def moveTowardsTarget(self):
        dy = self.y - self.targetY
        dx = self.targetX - self.x
        self.angle = math.atan2(dy, dx)
        self.move()

    def updateVelocity(self):
        if self.v == self.targetV:
            return
        elif self.v > self.targetV:
            self.v -= self.deaccel
            if self.v < self.targetV: self.v = self.targetV
        else:
            self.v += self.accel
            if self.v > self.targetV: self.v = self.targetV

