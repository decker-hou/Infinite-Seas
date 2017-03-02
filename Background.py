#responsible for drawing all the background non-interactable stuff
import pygame, math, random
from Utils import Utils
from gameSprite import GameSprite

class Background():
    def getColors(self, data, length):
        list = []
        for i in range(length):
            frac = i/(length-1)
            list.append(Utils.interpolateColor(Utils.BLUE,Utils.DARKBLUE,frac))
        return list

    def __init__(self, data):
        self.landHeight = data.landHeight
        self.waterLine = -1 * data.screenY

        self.skyCanvas = pygame.Surface([data.WIDTH, data.HEIGHT])
        self.skyCanvasW = data.STAGEWIDTH
        self.skyCanvasH = data.HEIGHT
        self.cloudParallax = 0.2
        self.backCloudParallax = 0.1
        self.cloudImg = pygame.image.load("assets/cloud.png")
        self.backCloudImg = pygame.image.load("assets/cloud2.png")
        self.numClouds = self.skyCanvasW // 300
        self.clouds = set()
        self.backClouds = set()

        for i in range(self.numClouds):
            rand = random.randint(-50, 50)
            x = i*300 + rand
            y = random.randint(self.skyCanvasH//2, self.skyCanvasH*7//8)
            self.clouds.add((x,y))

        for i in range(self.numClouds):
            rand = random.randint(-50, 50)
            x = i*300+100 + rand
            y = random.randint(self.skyCanvasH*3//4, self.skyCanvasH*7//8)
            self.backClouds.add((x,y))

        self.waterColor = Utils.BLUE
        self.colors = 30 #how many colors in the water gradient
        self.waterColors = self.getColors(data, self.colors) # list

        self.lightLayers = 3
        self.lightdX = 0

        self.lights = [] # needs to be ordered from back to front
        for layer in range(self.lightLayers):
            list = []
            for i in range(0, data.WIDTH, 200):
                w = 1.0 / (layer+1) #factor that changes light strip width
                list.append((i+random.randint(-100,100), 
                             random.randint(int(30*w),int(200*w)),
                             1/self.lightLayers*(layer+1))) #x, w, parallax
            self.lights.append(list)

    #if y coordinate of top edge is negative, then it's above the water
    #if it's positive then we don't see sky
    def update(self, data):
        self.waterLine = -1 * data.screenY
        index = math.floor(data.player.y / (data.STAGEHEIGHT/ self.colors))
        if index < 0: index = 0
        self.waterColor = self.waterColors[index]
        self.lightdX = self.lightdX + 0.3

    def drawOcean(self, data, surface):
        surface.fill(self.waterColor)
        for i in range(self.lightLayers):
            transparency = 0.15* (i+1)/self.lightLayers
            color = Utils.interpolateColor(self.waterColor, (255,255,255), 
                                          transparency)
            for (x, w, p) in self.lights[i]:
                x = (( x+data.WIDTH*1.2 + self.lightdX*p - data.screenX*p ) %
                    (data.WIDTH*1.2))
                #x1.2 prevents it from disappearing at edges
                pygame.draw.line(surface, color, (x-w, 0), 
                                (x-w+100, data.HEIGHT), w )

    #just solid walls that extend beyond the edge of the playing field
    def drawWalls(self, data, surface):
        (screenX, screenY) = data.screenX, data.screenY
        if screenY + data.HEIGHT >= data.STAGEHEIGHT:
            pygame.draw.rect(surface, (0,0,0), 
                (0, data.STAGEHEIGHT-screenY, data.WIDTH, data.HEIGHT))
        if screenX < 0: #left wall
            pygame.draw.rect(surface, (0,0,0),
                (0, max(0,-1*screenY-self.landHeight), 0-screenX, data.HEIGHT))
        elif screenX > data.WIDTH:
            pygame.draw.rect(surface, (0,0,0),
                (data.STAGEWIDTH-screenX, max(0, -1*screenY-self.landHeight),
                 data.WIDTH, data.HEIGHT))

    def drawSky(self, data, surface):
        if self.waterLine >= 0:
            self.skyCanvas.fill(Utils.SKY)
            for (x,y) in self.backClouds:
                self.skyCanvas.blit(self.backCloudImg, 
                    (x-data.screenX*self.backCloudParallax, y))

            for (x,y) in self.clouds:
                self.skyCanvas.blit(self.cloudImg, 
                    (x-data.screenX*self.cloudParallax, y))
            surface.blit(self.skyCanvas,(0,self.waterLine-self.skyCanvasH))

    def drawAll(self, data, surface):
        self.drawOcean(data, surface)
        self.drawSky(data, surface)
        self.drawWalls(data, surface)