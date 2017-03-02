import pygame
from button import Button
from Utils import Utils
from particle import Food

#a model class for managing the UI overlay in game. Items and some game 
#variables related to UI are kept track of here too

class UI():

    def __init__(self, data):
        self.items = []
        self.mode = "LOOK"
        self.currentItem = 0
        self.maxFood = 5
        self.food = self.maxFood

        self.depth = 0
        self.oxygen = 1.0
        self.oxygenRate = 0.002 #per second
        self.tooltipVisible = False
        self.tooltipText = ""

        self.hoverBoxText = "Test"
        self.infoBoxVisible = False
        self.infoSpecies = None

        self.width = data.WIDTH
        self.height = data.HEIGHT
        self.margin = 20

        self.oxyHeight = 150
        self.oxyY = 524
        self.oxygenRect = pygame.Rect(self.margin+22, self.oxyY-self.oxyHeight,
                          10, self.oxyHeight)
        self.images = set()
        invSprite = pygame.image.load("assets/inventory_bar.png")
        self.images.add((invSprite, (self.margin, self.height-self.margin-60)))
        oxySprite = pygame.image.load("assets/oxygen.png")
        self.images.add((oxySprite, (self.margin, 300)))
        self.infoBoxBg = pygame.image.load("assets/info_box.png")

        self.buttons = set()
        self.closeBtn = Button('assets/close_button.png', 680, 100, 
                        self.closeInfoBox, True, group=self.buttons)
        self.closeBtn.visible = False
        examineBtn = Button('assets/look_ui_button.png', 26, data.HEIGHT-74, 
                     self.examineBtnFn, group=self.buttons)
        food1Btn = Button('assets/food_ui_button.png', 86, data.HEIGHT-74, 
                   self.food1BtnFn, group=self.buttons)
        self.hoverBtn = Button('assets/hover.png',data.WIDTH//2,data.HEIGHT-40,
                        self.openInfoBox, True, group=self.buttons)
        self.hoverBtn.visible = False

        self.cursorSprite = pygame.image.load('assets/look_icon.png')
        self.returnSprite = pygame.image.load('assets/return_arrow.png')
        self.toolTipSprite = pygame.image.load('assets/tooltip.png')

    def examineBtnFn(self): 
            self.mode = "LOOK"
            self.currentItem = 0

    def food1BtnFn(self): 
            self.mode = "FOOD1"
            self.currentItem = 1

    def openInfoBox(self):
        self.infoBoxVisible = True
        self.closeBtn.visible = True

    def closeInfoBox(self):
        self.infoBoxVisible = False
        self.closeBtn.visible = False

    def update(self, data, event):
        if event.type == pygame.USEREVENT: #timer fired per second
            self.oxygen -= self.oxygenRate
            if self.oxygen < 0:
                data.exitDiveFn(data)
            else:
                self.oxygenRect.height = self.oxyHeight * self.oxygen
                self.oxygenRect.bottom = self.oxyY
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    button.onClick()
                    return

            fish = self.canTouchFish(data, pos)
            if fish == None:
                self.hoverBtn.visible = False
            else:
                self.hoverBtn.visible = True
                self.infoSpecies = fish.species
                self.hoverBoxText = (
                    fish.species.name if fish.species.discovered else "???")

            if self.mode == "FOOD1":
                if event.button == 3:
                    self.dropFood(data)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.examineBtnFn()
            elif event.key == pygame.K_2:
                self.food1BtnFn()
            elif event.key == pygame.K_SPACE:
                self.tooltipVisible = False

    def reset(self):
        self.oxygen = 1
        self.food = self.maxFood

    def dropFood(self, data):
        if self.food > 0:
            self.food -= 1
            data.foods.add(Food(data.player.x+20, data.player.y+21, 
                            data.player.direction))

    def canTouchFish(self, data, pos):
        if self.mode != "LOOK": return None
        if not data.player.isWithinInteractionRadius(pos[0],pos[1]):return None
        for school in data.schools:
            for fish in school.fishes:
                if fish.rect.collidepoint(pos): return fish
        return None

    def canCursorInteractWithFish(self, data, pos):
        fish = self.canTouchFish(data, pos)
        if fish == None: return False
        return fish.fed

    def openTooltip(self, text):
        self.tooltipText = text
        self.tooltipVisible = True


    def drawCustomCursor(self, data, surface):
        mousePos = pygame.mouse.get_pos()
        if (data.boat.rect.collidepoint(mousePos) 
          and data.player.isWithinInteractionRadius(mousePos[0], mousePos[1])):
            pygame.mouse.set_visible(False)
            surface.blit(self.returnSprite, mousePos)
        elif self.canCursorInteractWithFish(data, mousePos):
            pygame.mouse.set_visible(False)
            surface.blit(self.cursorSprite, mousePos)
        else:
            pygame.mouse.set_visible(True)

    def drawTooltip(self, surface):
        Utils.blitCenter(self.toolTipSprite, surface, (self.width//2, 
                         self.height//2))
        if isinstance(self.tooltipText, str):
            label = Utils.smallishFont.render(self.tooltipText, 1, Utils.WHITE)
            Utils.blitCenter(label, surface, (self.width//2, self.height//2))

    def drawHoverBoxText(self, surface):
        if isinstance(self.hoverBoxText, str):
            label = Utils.medSansFont.render(self.hoverBoxText, 1, Utils.WHITE)
            Utils.blitCenter(label, surface, (self.width//2, 
                             self.height-self.margin-20))

    def drawInfoBox(self, surface):
        Utils.blitCenter(self.infoBoxBg,surface,(self.width//2,self.height//2))
        self.infoSpecies.drawInfoBox(surface)

    def drawAll(self, data, surface):

        if self.tooltipVisible: self.drawTooltip(surface)
        if self.infoBoxVisible: self.drawInfoBox(surface)

        for (sprite, dest) in self.images:
            surface.blit(sprite, dest)
        pygame.draw.rect(surface, (255,0,0), self.oxygenRect)
        for button in self.buttons:
            button.draw(surface)

        if self.hoverBtn.visible: self.drawHoverBoxText(surface)

        #food number
        number = Utils.medSansFont.render(str(self.food), 1, Utils.BLACK)
        surface.blit(number, (26+60+33, self.height-47))
        #inv highlight rect
        pygame.draw.rect(surface, (255,255,0), (26+60*self.currentItem,
                        self.height - 74,48, 48), 3)

        self.drawCustomCursor(data, surface)

