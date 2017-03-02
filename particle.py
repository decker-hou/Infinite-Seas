import pygame, random, math
from pygame import gfxdraw
from Utils import Utils

class Particle():
    def __init__(self, x, y, v, angle, accel):
        self.x = x
        self.y = y
        self.v = v
        self.angle = angle
        self.accel = accel

    def update(self): #calls every frame
        if self.v >= 0:
            self.v += self.accel
            self.x += self.v * math.cos(self.angle)
            self.y -= self.v * math.sin(self.angle)

class FoodParticle(Particle):
    color = (160, 100, 0)
    def __init__(self, x, y, v, angle):
        super().__init__(x, y, v, angle, -0.005)
        self.size = random.randint(2,5)

    def draw(self, surface, data):
        pygame.draw.rect(surface, FoodParticle.color, (self.x-data.screenX, 
                        self.y-data.screenY, self.size, self.size))

class Bubble(Particle):
    color = (170, 200, 255)
    minR = 2
    maxR = 5
    def __init__(self, x, y, v):
        super().__init__(x, y, v, math.pi/2, 0.01)
        self.radius = random.randint(Bubble.minR, Bubble.maxR)

    def draw(self, surface, data):
        pygame.gfxdraw.aacircle(surface, int(self.x-data.screenX), 
                            int(self.y-data.screenY), self.radius, Bubble.color)
        pygame.gfxdraw.arc(surface, int(self.x-data.screenX), 
                int(self.y-data.screenY), self.radius, 210, 330, Utils.WHITE)

class WaterParticle(Particle):
    color = (30, 155, 210)
    def __init__(self, x, y, v, angle):
        super().__init__(x, y, v, angle, -0.1)
        self.vx = self.v * math.cos(self.angle)
        self.vy = self.v * math.sin(self.angle)
        self.size = random.randint(2,5)

    def draw(self, surface, data):
        pygame.draw.rect(surface, WaterParticle.color, (self.x-data.screenX, 
                                self.y-data.screenY, self.size, self.size))

    def update(self): #calls every frame
        self.vy += self.accel
        self.x += self.vx
        self.y -= self.vy

##############################

class Emitter():
    def __init__(self, x, y, particleClass):
        self.x = x
        self.bx = x
        self.y = y
        self.PClass = particleClass
        self.particles = []

    def update(self): #calls every frame
        for particle in self.particles:
            particle.update()

    def draw(self, surface, data):
        for particle in self.particles:
            particle.draw(surface, data)


class BubbleEmitter(Emitter):
    def __init__(self, x, y):
        super().__init__(x, y, Bubble)
        self.emitChance = 0.2
        self.t = 0 #ms

    def update(self, data):
        super().update()
        self.t += 16
        #6 sec breathing cycle
        if self.t > 6000: self.t = 0
        (self.x, self.y) = (data.player.x, data.player.y)
        self.bx = self.x+10 if data.player.direction == -1 else self.x+30
        if self.t > 3000 and random.random() < self.emitChance:
            #make new particles
            randX = random.randint(-5,5)
            self.particles.append(self.PClass(self.bx+randX, self.y+10, 0.0))

        #remove old particles
        self.particles = [p for p in self.particles if p.y >= p.radius]


class WaterEmitter(Emitter):
    def killEmitters(data):
        data.waterEmitters = set(e for e in data.waterEmitters 
                                 if e.particles != [])

    def __init__(self, x, y, v):
        super().__init__(x, y, WaterParticle)
        self.numParticles = int(80 * (v/4)) #splasiness scaled to player v
        self.maxV = 3 * v/4 #scaled to player v
        self.particles = self.makeParticles()

    def makeParticles(self):
        list = []
        for i in range(self.numParticles):
            angle = Utils.randomRange(math.pi/4, math.pi*3/4)
            rand = random.random()
            list.append(self.PClass(self.x, self.y, rand*self.maxV, angle))
        return list

    def update(self):
        super().update()
        self.particles = [p for p in self.particles if p.y < 0]


class Food(Emitter):
    def killEmitters(data):
        data.foods = set(food for food in data.foods if food.time < food.life)

    def __init__(self, x, y, direction):
        super().__init__(x, y, FoodParticle)
        self.direction = direction
        self.numParticles = 6
        self.life = 8
        self.time = 0

        self.particles = self.makeParticles()

    def secondUpdate(self, data):
        self.time += 1

    def makeParticles(self):
        list = []
        for i in range(self.numParticles):
            if self.direction == 1: angle = Utils.randomRange(-1*math.pi/6, 0)
            else: angle = Utils.randomRange(math.pi, math.pi*7/6)
            randX = random.randint(-5,5)
            randY = random.randint(-5,5)
            list.append(self.PClass(self.x+randX, self.y+randY, 0.5, angle))
        return list