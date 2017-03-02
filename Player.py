import pygame, math
from movingSprite import MovingSprite
from particle import WaterEmitter
from Utils import Utils


class Player(MovingSprite):
    def __init__(self, data, x, y):
        super().__init__(data, x, y, "assets/diver.png", 0, 0.06, 0.2)

        self.deaccel = 0.2

        self.minVDist = 50
        self.maxVDist = 300
        self.minV = 1
        self.maxV = 4
        self.interactionDistSq = 100**2

        self.rect.x = data.WIDTH // 2
        self.rect.y = data.HEIGHT // 2 #sprite location on screen


    def isLocationLegal(self, data):
        xLegal = self.x >= 0 and self.x < data.STAGEWIDTH
        yLegal = self.y <= data.STAGEHEIGHT #and self.y >= 0

        if not (xLegal and yLegal): return False

        return not data.wall.isColliding(self)

    #linear interpolation, returns target velocity based on mouse distance
    def getVelocityTargetFromMouseDist(self, dist):
        if dist < self.minVDist: return 0
        elif dist > self.maxVDist: return self.maxV
        else:
            distChange = self.maxVDist-self.minVDist
            distFraction = (dist-self.minVDist) / distChange
            vChange = self.maxV - self.minV
            return self.minV + distFraction*vChange

    def moveWithCollisions(self, data):
        (oldX, oldY) = self.x, self.y

        self.x += self.v * math.cos(self.angle)
        if not self.isLocationLegal(data):
            self.x = oldX
            assert(self.isLocationLegal(data) == True)

        self.y -= self.v * math.sin(self.angle)
        if not self.isLocationLegal(data):
            self.y = oldY
            assert(self.isLocationLegal(data) == True)

    def moveWithBounce(self, data):
        self.x += self.v * math.cos(self.angle)
        self.y -= self.v * math.sin(self.angle)
        if not self.isLocationLegal(data):
            self.angle += math.pi

    def moveJumping(self, data):
        vx = self.v * math.cos(self.angle)
        vy = self.v * math.sin(self.angle) - 0.08 #gravity
        self.v = math.sqrt(vx**2 + vy**2)
        self.angle = math.atan2(vy, vx)
        self.moveWithBounce(data)

    def moveTowardsMouse(self, x, y, data):
        dy = self.rect.y - y
        dx = x - self.rect.x
        self.angle = math.atan2(dy, dx)
        dist = Utils.distance(self.rect.x, self.rect.y, x, y)
        self.targetV = self.getVelocityTargetFromMouseDist(dist)
        self.updateVelocity()
        self.moveWithCollisions(data)
        self.doTurn(x+data.screenX) #turning sprite

    def deaccelInCurrentDirection(self, data):
        self.updateVelocity()
        self.moveWithCollisions(data)

    #return top left camera coords
    def doMove(self, data):
        oldY = self.y
        if self.y < 0:
            self.moveJumping(data)
        elif data.mouseHeld:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            self.moveTowardsMouse(mouseX, mouseY, data)

        elif self.v > 0: #mouse up, player slows down
            self.targetV = 0
            self.deaccelInCurrentDirection(data)

        newY = self.y
        if oldY*newY < 0 and self.v > 1: #one is neg, one is pos
            data.waterEmitters.add(WaterEmitter(self.x+20, 0, self.v))

        return (self.x-data.WIDTH/2, self.y-data.HEIGHT/2)

    #screen
    def isWithinInteractionRadius(self, x, y):
        return (Utils.distanceSq(x, y, self.rect.x, self.rect.y) 
                < self.interactionDistSq)

    #real coords
    def closeToInteract(self, x, y):
        return (Utils.distanceSq(x, y, self.x, self.y) < self.interactionDistSq)
