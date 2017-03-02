import pygame, random, math
from encyclopedia import Encyclopedia
from movingSprite import MovingSprite
from Utils import Utils

class Fish(MovingSprite):
    WANDER = "wander"
    FOLLOW = "follow"
    FEEDING = "feeding"
    FLEEING = "fleeing"
    REGROUP = "regroup"

    SPEEDS = {"wander": 0.4,
             "follow": 0.5,
             "feeding": 2,
             "fleeing": 5,
             "regroup": 1
            }

    ACCEL = 0.5
    DEACCEL = 0.3

    def collideFn(data, x, y, fish):
        if Utils.isRectOutOfStage(data, x, y,fish.rect.width,fish.rect.height):
            return True
        if data.wall.isCollidingLite(x, y, fish.mask): return True
        return Utils.lineWallCollision(data, int(x), int(y),
                                       int(fish.x), int(fish.y))

    def __init__(self,data,x,y,imgPath,school,direction=1, isLeader=False):
        super().__init__(data, x, y, imgPath, Fish.SPEEDS["wander"], 
                         Fish.ACCEL, Fish.DEACCEL)

        self.direction = direction
        if direction == -1:
            self.flipSprite()
        self.school = school #what school the fish is in
        self.isLeader = isLeader
        self.mode = Fish.WANDER if (self.isLeader) else Fish.FOLLOW
        self.fed = False
        self.justFed = False
        self.interactedWith = False #cannot be interacted with again if true
        self.species = school.info

        self.minTargetDist = 100
        self.maxTargetDist = 200
        self.maxFollowDist = 80
        self.turnChance = 0.2 #how likely it is to turn when wandering
        self.threatDist = 100
        self.foodDistSq = 150**2
        self.threatVel = 3.0 #how fast the player must be to scare the fish
        self.maxTargetUpdateAttempts = 40

        self.updateScreenCoords(data)
        #self.updateTarget()

    def __repr__(self):
        return self.school.info.__str__()

    #return an angle but tends towards the horizontal, will never point up
    #or down more than 30 degrees
    def getRandomWanderAngle(self):
        left = Utils.randomRange(-1*math.pi/6, math.pi/6)
        right = Utils.randomRange(5/6*math.pi, 7/6*math.pi)
        if self.direction == 1:
            return Utils.randomChoice(right, left, self.turnChance)
        else:
            return Utils.randomChoice(left, right, self.turnChance)

    def getFleeingAngle(self, otherX, otherY):
        #opposite angle of the threat
        oppAngle = Utils.getAngle(self.x, self.y, otherX, otherY) - math.pi
        return Utils.randomRange(oppAngle-math.pi/6, oppAngle+math.pi/6)

    def updateTargetVelocity(self):
        self.targetV = Fish.SPEEDS[self.mode]

    def coordsFromDistAngle(self, x, y, dist, angle):
        return (x + dist * math.cos(angle), y - dist * math.sin(angle))

    def justChooseAnyTarget(self):
        dist = random.randrange(0, self.maxTargetDist)
        angle = Utils.randomRange(0, 2*math.pi)
        return self.coordsFromDistAngle(self.x, self.y, dist, angle)

    def chooseNewTarget(self, data):
        if self.mode == Fish.WANDER:
            dist = random.randrange(self.minTargetDist, self.maxTargetDist)
            angle = self.getRandomWanderAngle()
            return self.coordsFromDistAngle(self.x, self.y, dist, angle)

        elif self.mode == Fish.FOLLOW:
            leader = self.school.getLeader()

            dist = random.randrange(0, self.maxFollowDist)
            angle = Utils.randomRange(0, 2*math.pi)
            return self.coordsFromDistAngle(leader.x, leader.y, dist, angle)

        elif self.mode == Fish.FLEEING:
            dist = random.randrange(self.minTargetDist, self.maxTargetDist)
            angle = self.getFleeingAngle(data.player.x, data.player.y)
            return self.coordsFromDistAngle(self.x, self.y, dist, angle)

        elif self.mode == Fish.FEEDING:
            return self.foodLocation

    #try choosing new targets until you get a legal one
    def updateTarget(self, data):
        self.updateTargetVelocity()
        #pick target according to mode
        tries = 0
        while (tries < self.maxTargetUpdateAttempts):
            tries += 1
            (targetX, targetY) = self.chooseNewTarget(data)
            #this new target is fine
            if not Fish.collideFn(data, targetX, targetY, self):
                self.setTarget(targetX, targetY)
                return

        #failed to choose a target, just try going anywhere instead of
        #getting stuck forever
        while (True):
            (targetX, targetY) = self.justChooseAnyTarget()
            if not Fish.collideFn(data, targetX, targetY, self):
                self.setTarget(targetX, targetY)
                return

    def playerDangerSensed(self, data):
        player = data.player
        return (player.v > self.threatVel and Utils.distance(self.x, self.y, 
            player.x, player.y) < self.threatDist)

    def foodSensed(self, data):
        if self.justFed: return False
        for food in data.foods:
            if Utils.distanceSq(self.x, self.y, food.x, food.y)<self.foodDistSq: 
                foodParticle = random.choice(food.particles)
                self.foodLocation = (foodParticle.x, foodParticle.y)
                return True
        return False

    def doMove(self, data):
        self.updateVelocity()
        oldDist = Utils.distanceSq(self.x, self.y, self.targetX, self.targetY)
        self.moveTowardsTarget()
        newDist = Utils.distanceSq(self.x, self.y, self.targetX, self.targetY)

        if self.playerDangerSensed(data) and self.mode != Fish.FLEEING: 
            #fuck that, time to get out of here
            self.mode = Fish.FLEEING
            self.updateTarget(data)

        elif (self.foodSensed(data) and self.mode != Fish.FEEDING 
              and self.mode != Fish.FLEEING):
            self.mode = Fish.FEEDING
            self.updateTarget(data)

        if (newDist >= oldDist): #arrived at target
            if self.mode == Fish.FLEEING: #cools off
                self.mode = Fish.WANDER if (self.isLeader) else Fish.FOLLOW

            elif self.mode == Fish.FEEDING: #arrives at food
                self.fed = True
                self.justFed = True
                self.mode = Fish.WANDER if (self.isLeader) else Fish.FOLLOW
            else:
                self.justFed = False

            self.updateTarget(data)

    def canInteract(self):
        return (self.fed and self.mode != Fish.FLEEING 
                and self.species.canInteractWith())

    def onClick(self, data):
        species = self.species
        if self.canInteract():
            species.canInteract = False
            if not species.discovered:
                text = "New species discovered!"
            elif species.factsDiscovered < 3:
                text = "New fact discovered!"
            else:
                text = "You've learned everything about this species."
            data.ui.openTooltip(text)
            species.interact(data)

    def drawDebug(self, data, surface):
        x = int(self.targetX - data.screenX)
        y = int(self.targetY - data.screenY)
        if self.mode == Fish.WANDER:
            color = (255,255,0)
        elif self.mode == Fish.FOLLOW:
            color = (100,255,0)
        elif self.mode == Fish.FLEEING:
            color = (255,0,0)
        else:
            color = (255, 50, 255)
        pygame.draw.line(surface, Utils.WHITE,(x,y),(self.rect.x, self.rect.y))
        pygame.draw.circle(surface, color, (x,y), 3)


#A school class has a list of fish. All fish belong to schools, School object
#is responsible for initial placement.
class School():
    MAX_DIST = 100

    def placeFish(data):
        data.schools = []
        for species in data.encyclopedia.speciesList:
            t = 0
            while True:
                t += 1
                assert(t<100)
                x = random.randrange(0, data.STAGEWIDTH)
                y = random.randrange(0, data.STAGEHEIGHT)
                if not data.wall.isCollidingLite(x, y, species.mask):
                    break
            school = School(data, x, y, species)
            data.schools.append(school)
            for fish in school.fishes:
                data.fishSprites.add(fish)

    def __init__(self, data, x, y, species):
        self.info = species #rename to species?
        leaderFish = Fish(data, x, y, self.info.imgPath, self, isLeader=True)
        self.fishes = [leaderFish]

        if self.info.groupSize > 1:
            self.populateFish(data, x, y, self.info.groupSize-1)

    def getLeader(self):
        return self.fishes[0]

    def isPositionLegal(self, data, x, y):
        if not (x > 0 and y > 0 and x<data.STAGEWIDTH and y<data.STAGEHEIGHT):
            return False
        return not data.wall.isCollidingLite(x, y, self.info.mask)

    #given a location and amount of fish, return set of x,y tuples
    #of appropriate places to place fish
    def createFishLocations(self, data, x, y, amount):
        coords = set()
        fishPlaced = 0
        fish = Fish(data, 0, 0, self.info.imgPath, self)
        #let's just do random sampling for now
        while fishPlaced < amount:
            fishX = x + random.randint(-1*School.MAX_DIST, School.MAX_DIST)
            fishY = y + random.randint(-1*School.MAX_DIST, School.MAX_DIST)
            if self.isPositionLegal(data, fishX, fishY):
                coords.add((fishX, fishY))
                fishPlaced += 1
        return coords

    def populateFish(self, data, x, y, amount):
        coords = self.createFishLocations(data, x, y, amount)
        for (fishX, fishY) in coords:
            self.fishes.append(Fish(data, fishX, fishY, self.info.imgPath,self))

    def markInteracted(self, data):
        data.encyclopedia.markSpeciesInteracted(self.info.name)

    def moveAll(self, data):
        for fish in self.fishes:
            fish.doMove(data)
