import pygame
from gameSprite import GameSprite

class Wall(GameSprite):
    def __init__(self, data, x, y, img):
        super().__init__(data, x, y, img)
        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey((255,255,255))
        self.mask = pygame.mask.from_surface(self.image)

    #other is a GameSprite
    def isColliding(self, other):

        #overlap function only takes ints
        (offsetX, offsetY) = (int(other.x-self.x), int(other.y - self.y))
        overlap = self.mask.overlap(other.mask, (offsetX, offsetY))
        return (overlap != None)

    def isCollidingLite(self, x, y, mask):
        (offsetX, offsetY) = (int(x-self.x), int(y - self.y))
        overlap = self.mask.overlap(mask, (offsetX, offsetY))
        return (overlap != None)

    def draw(self, surface):
        surface.blit(self.image, self.rect)