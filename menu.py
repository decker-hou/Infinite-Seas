import sys, pygame, random
from button import Button
from Background import Background
from Utils import Utils

pygame.init()

#A Menu has a set of buttons. It handles drawing and listening to events for
#its buttons 
class Menu():
    def __init__(self, data):
        self.buttons = set()
        random.seed("42")
        self.oceanBg = Background(data)
        random.seed()

    def update(self, data, event):
        if event.type == pygame.USEREVENT+1:
            self.oceanBg.update(data)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    button.onClick(data)

    def draw(self, data, surface):
        self.oceanBg.drawOcean(data, surface)
        self.oceanBg.drawSky(data, surface)
        for button in self.buttons:
            button.draw(surface)

#Each actual menu in the game is a class inherited from Menu
class GameMenu(Menu):
    def __init__(self, data):
        super().__init__(data)

        def diveBtnFn(data): data.newDiveFn(data)
        diveBtn = Button('assets/dive_button.png',data.WIDTH//2,
                        data.HEIGHT//3, diveBtnFn, True, group=self.buttons)

        def helpBtnFn(data): data.gameMode = "TUTORIAL"
        helpBtn = Button('assets/tutorial_button.png',data.WIDTH//2,
                        data.HEIGHT//2, helpBtnFn, True, group=self.buttons)

        def encBtnFn(data): data.gameMode = "ENCYCLOPEDIA"
        encBtn = Button('assets/encyclopedia_button.png', data.WIDTH//2,
                        data.HEIGHT*2//3, encBtnFn, True, group=self.buttons)

        def backBtnFn(data): 
            data.saveFn(data)
            data.gameMode = "SPLASH"
        backBtn = Button('assets/main_menu_button.png', data.WIDTH//2,
                        data.HEIGHT*5//6, backBtnFn, True, group=self.buttons)

class SplashMenu(Menu):
    def __init__(self, data):
        super().__init__(data)
        self.title = pygame.image.load('assets/title.png')

        def newBtnFn(data): 
            data.newGameFn(data)
        newBtn = Button('assets/new_button.png',data.WIDTH//2,
                 data.HEIGHT//3, newBtnFn, True, group=self.buttons)

        def createBtnFn(data): 
            data.creator.reset()
            data.gameMode = "CREATE"
        createBtn = Button('assets/create_button.png',data.WIDTH//2,
                    data.HEIGHT//2, createBtnFn, True, group=self.buttons)

        def loadBtnFn(data): data.loadFn(data)
        loadBtn = Button('assets/load_button.png',data.WIDTH//2,
                  data.HEIGHT*2//3, loadBtnFn, True, group=self.buttons)

        def quitBtnFn(data):
            pygame.quit()
            sys.exit()
        quitBtn = Button('assets/quit_button.png',data.WIDTH//2,
                  data.HEIGHT*5//6, quitBtnFn, True, group=self.buttons)

    def draw(self, data, surface):
        super().draw(data, surface)
        Utils.blitCenter(self.title, surface, (data.WIDTH//2, data.HEIGHT//6))

class TutMenu(Menu):
    def __init__(self, data):
        super().__init__(data)
        img1 = pygame.image.load('assets/tutorial1.png')
        img2 = pygame.image.load('assets/tutorial2.png')
        img3 = pygame.image.load('assets/tutorial3.png')
        self.images = [img1, img2, img3]
        self.index = 0

        def prevBtnFn(data): 
            self.index -= 1
            if self.index <= 0: self.prevBtn.visible = False
        self.prevBtn = Button('assets/arrow_left.png',20,
                 data.HEIGHT-100, prevBtnFn, group=self.buttons)
        self.prevBtn.visible = False

        def nextBtnFn(data):
            self.prevBtn.visible = True
            if self.index == 2:
                data.gameMode = "MENU"
                self.index == 0
            else: self.index += 1
        self.nextBtn = Button('assets/arrow_right.png',data.WIDTH-60,
                 data.HEIGHT-100, nextBtnFn, group=self.buttons)

    def draw(self, data, surface):
        surface.blit(self.images[self.index], (0,0))
        for button in self.buttons:
            button.draw(surface)
