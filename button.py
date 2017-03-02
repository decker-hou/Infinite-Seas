import pygame

#Code is based off and heavily modified from the article found at:
#http://inventwithpython.com/blog/2012/10/30/creating-a-button-ui-module
#-for-pygame/

class Button(pygame.sprite.Sprite):
    def __init__(self, imgPath, x, y, clickFn, center=False, selfRef=False,
                 group=None):
        self.clickFn = clickFn
        self.selfRef = selfRef
        self.image = pygame.image.load(imgPath).convert_alpha()
        self.rect = self.image.get_rect()
        self.selected = False
        self.highLightClr = (255,255,0)
        if center == True:
            self.rect.x = x - self.rect.width//2
            self.rect.y = y - self.rect.height//2
        else:
            self.rect.x = x
            self.rect.y = y
        self.visible = True

        if group != None:
            group.add(self)

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            if self.selected:
                pygame.draw.rect(surface, self.highLightClr, self.rect, 3)

    def onClick(self, *args):
        if self.visible:
            if self.selfRef:
                self.clickFn(self, *args)
            else:
                self.clickFn(*args)
