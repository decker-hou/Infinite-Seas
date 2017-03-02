import pygame

#some extra functionalities for pygame sprites
#has mask collision, and calculating position on screen from scrolling
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, data, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.x = x
        self.y = y

        self.updateScreenCoords(data)

    def updateScreenCoords(self, data):
        self.rect.x = self.x - data.screenX
        self.rect.y = self.y - data.screenY