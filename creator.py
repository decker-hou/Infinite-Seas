import pygame
from button import Button
from terrain import Terrain
from Utils import Utils

class Creator():
    def __init__(self, data):
        self.STAGEWIDTH = data.STAGEWIDTH
        self.STAGEHEIGHT = data.STAGEHEIGHT
        self.xImg = pygame.image.load('assets/x.png')

        self.width = 1000
        self.height = 500
        self.buttons = set()
        self.brushSelected = False
        self.brushColor = Utils.BLACK
        self.brushSize = 20
        self.mouseHeld = False
        self.lastPos = None

        def backBtnFn(data): data.gameMode = "SPLASH"
        backBtn = Button('assets/back_small.png', 20,
                        data.HEIGHT-50, backBtnFn, group=self.buttons)

        def saveBtnFn(data): 
            self.saveCanvas("saves/save0")
            data.loadFn(data)
            data.gameMode = "MENU"
        saveBtn = Button('assets/save_small.png',data.WIDTH-120,data.HEIGHT-50,
                         saveBtnFn, group=self.buttons)

        def drawBtnFn(data): 
            self.brushSelected = True
            self.drawBtn.selected = True
            self.eraseBtn.selected = False
            self.brushColor = Utils.BLACK
        self.drawBtn = Button('assets/paint_button.png', 200, data.HEIGHT-60, 
                        drawBtnFn, group=self.buttons)

        def eraseBtnFn(data): 
            self.brushSelected = True
            data.creator.drawBtn.selected = False
            data.creator.eraseBtn.selected = True
            self.brushColor = Utils.WHITE
        self.eraseBtn = Button('assets/erase_button.png', 260, data.HEIGHT-60, 
                        eraseBtnFn, group=self.buttons)

        self.sizes = [3,6,12,15,30,60,90]
        self.makeSizeBtns(data)

        self.bCanvas = pygame.Surface((data.WIDTH, data.HEIGHT))
        self.drawBCanvas()

        self.tCanvas = pygame.Surface((data.STAGEWIDTH, 
                        data.STAGEHEIGHT+data.landHeight)) #full sized canvas
        self.tSmall = pygame.Surface((self.width,self.height)) #screen sized
        self.tSmall.set_colorkey(Utils.WHITE) 
        self.terrain = Terrain(data.STAGEWIDTH,data.STAGEHEIGHT+data.landHeight)
        self.makeTCanvas()

    def makeSizeBtns(self, data):
        for i in range(len(self.sizes)):
            def btnFn(data, i=i): self.brushSize = self.sizes[i]
            btn = Button('assets/30x30.png', 350+i*31, data.HEIGHT-30, btnFn, 
                         True, group=self.buttons)

            def newDraw(surface, i=i):
                pygame.draw.circle(surface, Utils.BLACK, 
                                  (350+i*31, data.HEIGHT-30), (i+1)*2)

            btn.draw = newDraw

    def reset(self):
        self.brushSelected = False
        self.brushSize = 20
        self.drawBtn.selected = False
        self.eraseBtn.selected = False
        self.makeTCanvas()

    def drawBCanvas(self): #only needs to be called once
        self.bCanvas.fill(Utils.BLUE)
        pygame.draw.rect(self.bCanvas, Utils.SKY, (0, 0, self.width, 33))
        pygame.draw.rect(self.bCanvas, Utils.WHITE, (0, self.height, 
                         self.width, self.height))
        self.bCanvas.blit(self.xImg, (100,23))

    def makeTCanvas(self):
        self.terrain.newTerrain()
        self.terrain.drawBasicTerrain(self.tCanvas, Utils.BLACK)

    def saveCanvas(self, fileName): 
        pygame.image.save(self.tCanvas, fileName+"_stage.png")
        self.terrain.exportBg(fileName)

    def draw(self, data, surface):
        pygame.transform.scale(self.tCanvas, (self.width, self.height), 
                               self.tSmall)

        surface.blit(self.bCanvas, (0,0))
        surface.blit(self.tSmall, (0,0))

        for button in self.buttons:
            button.draw(surface)

    def update(self, data, event):
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseHeld = True
            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    button.onClick(data)
                    return

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouseHeld = False
            self.lastPos = None

        if pos[1]<= self.height: #over the canvas:
            pos = (pos[0]*3, pos[1]*3)
            if self.mouseHeld and self.brushSelected:
                pygame.draw.circle(self.tCanvas, self.brushColor, pos, 
                                    self.brushSize)
                if self.lastPos != None:
                    pygame.draw.line(self.tCanvas,self.brushColor,self.lastPos,
                                     pos, self.brushSize*2)
                self.lastPos = pos

