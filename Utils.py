import math, random, pygame

class Utils():
    pygame.init()
    smallFont = pygame.font.SysFont("serif", 12)
    smallishFont = pygame.font.SysFont("serif", 14)
    medFont = pygame.font.SysFont("serif", 16)
    largishFont = pygame.font.SysFont("serif", 20)
    bigFont = pygame.font.SysFont("serif", 42)
    medSansFont = pygame.font.SysFont("Arial", 16)

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GRAY = (40, 50, 60)
    BLUE = (30, 155, 210)
    DARKBLUE = (30, 90, 130)
    LIGHTBLUE = (50, 170, 230)
    SKY = (170, 200, 255)

    #from course website
    def almostEqual(n1, n2, epsilon=10**-4):
        return abs(n1-n2) < epsilon

    #gets dist between two coords
    def distance(x0, y0, x1, y1):
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)
        return math.sqrt(dx**2 + dy**2)

    def distanceSq(x0, y0, x1, y1):
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)
        return dx**2 + dy**2

    #gets random float between range
    def randomRange(min, max):
        return min + random.random()*(max-min)

    #gets weight random choice between two things
    def randomChoice(n1, n2, weight=0.5):
        return n1 if (random.random() < weight) else n2

    #get angles between two coords
    def getAngle(x, y, otherX, otherY):
        dy = y - otherY
        dx = otherX - x
        return math.atan2(dy, dx)

    def blitCenter(source, dest, location):
        rect = source.get_rect()
        rect.center = location
        dest.blit(source, rect)

    def isRectOutOfStage(data, x, y, w, h):
        return (x<0 or y<0 or x+w > data.STAGEWIDTH or y+h > data.STAGEHEIGHT)

    #frac is a number between 0 and 1, returns a RGB tuple
    def interpolateColor(color1, color2, frac):
        result = []
        for i in range(3): #srsly is this a magic number or not
            diff = color2[i] - color1[i]
            result.append(color1[i] + diff*frac)
        return tuple(result)

    #samples positions along the line uniformly and checks point collision
    #at each one.
    def lineWallCollision(data, x0, y0, x1, y1):
        dist = max(abs(x0-x1), abs(y0-y1))
        for t in range(1, dist, 2):
            x = int(x0 + t/dist * (x1 - x0))
            y = int(y0 + t/dist * (y1 - y0))
            if data.wall.mask.get_at((x,y+data.landHeight)) != 0: return True
        return False

    #break string down into lines no longer than maxWidth characters, does
    #not cut off words in the middle.
    def breakIntoLines(str,maxWidth):
        result = []
        words = str.split(" ")
        line = ""
        for word in words:
            if (len(line) + len(word) > maxWidth):
                result.append(line)
                line = ""
            line += word + " "
        result.append(line)
        return result

    def drawText(str, surface, x, y, font, color, center=False):
        label = font.render(str, 1, color)
        if center:
            Utils.blitCenter(label, surface, (x, y))
        else:
            surface.blit(label, (x, y))

    def drawMultilineText(str, surface, x,y, font, width, color, centerX=False):
        if len(str) <= width: 
            Utils.drawText(str, surface, x, y, font, color, centerX)
        else:
            lines = Utils.breakIntoLines(str, width)
            height = font.get_linesize()
            for i in range(len(lines)):
                Utils.drawText(lines[i], surface, x, y+i*height, 
                                font, color, centerX)
