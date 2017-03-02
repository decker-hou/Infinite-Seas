#the class that generates terrain and saves it as an image
import pygame
import random, copy, math
from Utils import Utils


class Coral():
    colors = [(250,20,80),(230,200,10),(255,155,40), (145, 240, 80),
             (255,160,200),(60,180,100),(120,70,190)]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(Coral.colors)

        self.w = 1
        self.depth = random.randint(4,6)
        self.minAngle = 0
        self.maxAngle = Utils.randomRange(0.6, 1)
        self.reduction = Utils.randomRange(0.3, 0.5)
        self.branchLen = random.randint(10, 20)

        self.coral = self.getTree()

    def randAngle(self):
        return Utils.randomRange(self.minAngle, self.maxAngle)

    def makeTree(self, x, y, angle, depth):
        if depth == 0:
            return []
        else:
            lenFactor = 0.8**(self.depth-depth)
            x2 = x - int(self.branchLen*lenFactor* math.cos(angle))
            y2 = y - int(self.branchLen*lenFactor* math.sin(angle))

            left = self.makeTree(x2, y2, angle-self.randAngle(), depth-1)
            right = self.makeTree(x2, y2, angle+self.randAngle(), depth-1)
            return left +  right + [((x, y), (x2, y2), self.w*depth)]

    def getTree(self):
        return (self.makeTree(self.x, self.y, math.pi/2-self.randAngle(), 
                self.depth) + self.makeTree(self.x, self.y, 
                math.pi/2+self.randAngle(), self.depth) )

    def draw(self, surface):
        for ((x0,y0),(x1,y1),width) in self.coral:
            pygame.draw.line(surface, self.color, (x0, y0), (x1, y1), width)

#Used midpoint displacement algorithm tutorial found at: 
#http://www.somethinghitme.com/2013/11/11/simple-2d-terrain-
#with-midpoint-displacement/
#code is original
class Terrain():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.minHeight = self.height // 3 * 2 #floor of terrain
        self.maxHeight = 0
        self.iterations = 6 #1 at minimum
        self.bumpiness = 25
        self.dampening = 0.5 #higher = more jagged

        self.peakDist = 3 #islands cannot spawn right at edge
        self.numOfCaves = 4
        self.caveWidth = 100
        self.caveHeight = 60
        self.caveMargin = 150 #dist of cave from edge
        self.yMargin = 60
        self.caveDist = 200 #dist between caves
        self.cavePoints = 60
        self.caveBumpiness = 4
        self.tunnelWidth = 60
        self.coralChance = 0.1

        self.vertices = []
        self.terrainPoints = self.getTopPoints()
        self.canvas = pygame.Surface((self.width,self.height))
        #self.caveCoords = self.getCaveCoords()

    #returns a list of coordinates of the terrain along the top
    def getTopPoints(self):
        points = [(0,self.maxHeight)]
        numOfPoints = 16 #initial vertices, controls edge slope steepness

        peak = random.randint(5,numOfPoints-self.peakDist-1)

        #creating the basic outline with a random peak or two
        for i in range(1, numOfPoints):
            x = self.width / numOfPoints * i
            offset = Utils.randomRange(-1*self.bumpiness, self.bumpiness)
            y = self.maxHeight if (i==peak or i==peak+1) else self.minHeight
            points.append((x, y+offset))

        #using midpoint displacement
        for n in range(1, self.iterations):
            xWidth = (points[1][0] - points[0][0]) / 2
            newPoints = []
            offsetLimit = int(self.bumpiness * ( self.dampening**n ))
            #generate a bunch of new points
            for i in range(len(points)-1):
                x = points[i][0] + xWidth
                (y0, y1) = (points[i][1], points[i+1][1])
                interpolatedY = y0 + ( (y1-y0) / 2 )
                offset = Utils.randomRange(-1*offsetLimit, offsetLimit)
                y = interpolatedY + offset
                newPoints.append((x,y))

            #now fold them back into the points list alternatingly
            temp = []
            for i in range(len(newPoints)):
                temp.append(points[i])
                temp.append(newPoints[i])
            temp.append(points[-1])

            points = copy.copy(temp)

        points.append((self.width, 0))
        return points

    def getCaveCoords(self):
        list = []
        for i in range(self.numOfCaves):
            while True:
                tooClose = False
                x = random.randint(self.caveMargin, self.width-self.yMargin)
                y = random.randint(self.minHeight+self.caveMargin, 
                                    self.height - self.caveMargin)
                for (roomX, roomY) in list:
                    if Utils.distance(x, y, roomX, roomY) < self.caveDist:
                        tooClose = True
                if not tooClose:
                    list.append((x,y))
                    break
        return sorted(list)

    def getCavePoints(self):
        def f(t, mult, add): 
            return (self.caveWidth*mult + add) * math.cos(2*math.pi*t)
        def g(t, mult, add): 
            return (self.caveHeight*mult + add) * math.sin(2*math.pi*t)
        list = []
        for (cx, cy) in self.caveCoords:
            cavePolygon = []
            sizeMultiplier = Utils.randomRange(0.7, 1.5)
            for i in range(self.cavePoints):
                t = i/self.cavePoints
                x = (f(t, sizeMultiplier, random.randint(-1*self.caveBumpiness,
                        self.caveBumpiness)) + cx)
                y = (g(t, sizeMultiplier, random.randint(-1*self.caveBumpiness,
                        self.caveBumpiness)) + cy)
                cavePolygon.append((x,y))
            list.append(cavePolygon)
        return list

    def drawBasicTerrain(self, surface, color):
        #adding bottom two corners
        self.vertices = ([(0, self.height)] + self.terrainPoints +
                         [(self.width, self.height)])
        surface.fill(Utils.WHITE)
        pygame.draw.polygon(surface, color, self.vertices)

    def drawCorals(self, surface):
        for (x, y) in self.terrainPoints:
            if random.random() < self.coralChance and y > 140:
                coral = Coral(x, y)
                coral.draw(surface)

    def drawCaves(self, surface):
        cavePolygons = self.getCavePoints()
        for cave in cavePolygons:
            pygame.draw.polygon(surface, Utils.WHITE, cave)

    def drawTunnels(self, surface):
        #tunnel through the peak
        pygame.draw.line(surface, Utils.WHITE, (100, self.height//3), 
                         (self.width-100, self.height//3), self.tunnelWidth)

        #tunnel through the first cave
        (cave1x, cave1y) = self.caveCoords[0]
        pygame.draw.line(surface, Utils.WHITE, (cave1x, cave1y), (cave1x, 0), 
                        self.tunnelWidth)

        #tunnels connecting caves
        for i in range(len(self.caveCoords)-1):
            pygame.draw.line(surface, Utils.WHITE, self.caveCoords[i], 
                                self.caveCoords[i+1], self.tunnelWidth)

    def newTerrain(self):
        self.terrainPoints = self.getTopPoints()

    def exportBg(self, fileName):
        self.drawBasicTerrain(self.canvas, Utils.GRAY)
        self.drawCorals(self.canvas)
        pygame.image.save(self.canvas, fileName+"_bg.png")

    def export(self, fileName):
        self.exportBg(fileName)

        self.drawBasicTerrain(self.canvas, Utils.BLACK)
        self.caveCoords = self.getCaveCoords()
        self.drawCaves(self.canvas)
        self.drawTunnels(self.canvas)
        pygame.image.save(self.canvas, fileName+"_stage.png")
