import os, sys
import pygame
import random, copy, math
import pickle
from pygame.locals import *

from Player import Player
from Background import Background
from fish import Fish, School
from encyclopedia import Encyclopedia 
from terrain import Terrain
from ui import UI
from wall import Wall
from Utils import Utils
from menu import GameMenu, SplashMenu, TutMenu
from gameSprite import GameSprite
from creator import Creator
from particle import Food, BubbleEmitter, WaterEmitter

#Basic pygame structure code adapted from this tutorial:
#http://www.nerdparadise.com/tech/python/pygame/basics/part1/

class Struct(object): pass
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH,HEIGHT))
clock = pygame.time.Clock()
FPS = 60
pygame.time.set_timer(USEREVENT, 1000)
pygame.time.set_timer(USEREVENT+1, 1000//FPS)


def init(data):
    data.font = pygame.font.SysFont("monospace", 15)
    data.STAGEHEIGHT = 1400
    data.STAGEWIDTH = 3000 

    data.landHeight = 100 #how far the land is above the sea in pixels

    (playerX, playerY) = (300, 0)
    data.screenX = playerX - data.WIDTH/2 #the camera
    data.screenY = playerY - data.HEIGHT/2

    #game objects
    data.fishSprites = pygame.sprite.Group()
    data.bgSprites = pygame.sprite.Group()
    data.bgStageSprites = pygame.sprite.GroupSingle()
    data.stageSprites = pygame.sprite.GroupSingle()
    data.playerSprite = pygame.sprite.GroupSingle()

    #all sprites that scroll
    data.gameSpriteGroups = [data.fishSprites, 
                             data.bgSprites, 
                             data.bgStageSprites, 
                             data.stageSprites]

    data.player = Player(data, playerX, playerY)
    data.playerSprite.add(data.player)

    data.bubbleEmitter = BubbleEmitter(playerX, playerY)
    data.waterEmitters = set()
    data.foods = set()

    data.boat = GameSprite(data, data.player.x, -120, "assets/boat.png")
    data.bgSprites.add(data.boat)

    data.terrain = Terrain(data.STAGEWIDTH, data.STAGEHEIGHT+data.landHeight)
    data.ui = UI(data)
    data.menu = GameMenu(data)
    data.splash = SplashMenu(data)
    data.tutorial = TutMenu(data)
    data.encyclopedia = Encyclopedia(data)
    data.creator = Creator(data)
    data.oceanBg = Background(data)

    data.mouseHeld = False
    data.gameMode = "SPLASH"

    data.newGameFn = newGame
    data.saveFn = save
    data.loadFn = load
    data.newDiveFn = newDive
    data.exitDiveFn = exitDive

def newDive(data):
    data.fishSprites.empty() #delete fish
    School.placeFish(data) #respawn new fish
    data.encyclopedia.resetSpeciesInteract()
    data.ui.reset()
    data.gameMode = "GAME"

def save(data):
        pickle.dump(data.encyclopedia.speciesDiscovered, 
                    open("saves/save0.p", "wb"))
        print("saved!")

def load(data):
    if os.path.isfile("saves/save0.p"):
        loadWalls(data, "saves/save0")
        data.encyclopedia.speciesDiscovered = pickle.load(
                                    open("saves/save0.p", "rb"))
        data.encyclopedia.reloadSpecies()
        data.gameMode = "MENU"

#resets encyclopedia information and background save files
def newGame(data):
    data.terrain.export('saves/save0')
    loadWalls(data, 'saves/save0')
    data.encyclopedia.resetDiscoveries()
    data.encyclopedia.resetSpeciesInteract()
    data.gameMode = "MENU"

def loadWalls(data, fileName):
    data.stageSprites.empty()
    data.bgStageSprites.empty()

    data.wall = Wall(data, 0, -1*data.landHeight, fileName+"_stage.png")
    data.wallBg = GameSprite(data, 0, -1*data.landHeight, fileName+"_bg.png")
    data.wallBg.image = pygame.image.load(fileName+"_bg.png").convert()
    data.wallBg.image.set_colorkey((255,255,255))

    data.stageSprites.add(data.wall)
    data.bgStageSprites.add(data.wallBg)

def exitDive(data):
    pygame.mouse.set_visible(True)
    data.gameMode = "MENU"

def drawCoords(data):
    text = "%f, %f" % (data.player.v, data.player.targetV)
    label = data.font.render(text, 1, Utils.BLACK)
    canvas.blit(label, (0,0))

def updateSpritesScreenPos(data):
    for group in data.gameSpriteGroups:
        for sprite in group:
            sprite.updateScreenCoords(data)

def drawSprites(data):

    data.bgSprites.draw(canvas)
    data.bgStageSprites.draw(canvas)
    data.bubbleEmitter.draw(canvas, data)
    #for fish in data.fishSprites:
    #    fish.drawDebug(data, canvas)
    data.fishSprites.draw(canvas)
    data.stageSprites.draw(canvas)
    for food in data.foods:
        food.draw(canvas, data)
    for emitter in data.waterEmitters:
        emitter.draw(canvas, data)
    data.playerSprite.draw(canvas)

def drawUI(data):
    data.ui.drawAll(data, canvas)

def gameDrawAll(data):
    data.oceanBg.drawAll(data, canvas)
    drawSprites(data)
    #drawCoords(data)
    drawUI(data)
    screen.blit(canvas, (0,0))

def redrawAll(data):
    if data.gameMode == "GAME":
        gameDrawAll(data)
    elif data.gameMode == "ENCYCLOPEDIA":
        data.encyclopedia.draw(screen)
    elif data.gameMode == "SPLASH":
        data.splash.draw(data, screen)
    elif data.gameMode == "MENU":
        data.menu.draw(data, screen)
    elif data.gameMode == "CREATE":
        data.creator.draw(data, screen)
    elif data.gameMode == "TUTORIAL":
        data.tutorial.draw(data, screen)
    pygame.display.flip()

def gameModeUpdate(data, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            data.mouseHeld = True
        elif event.button == 3: #right click
            if data.player.isWithinInteractionRadius(pos[0],pos[1]): 
                if data.boat.rect.collidepoint(pos):
                    exitDive(data)
                fishClicked = data.ui.canTouchFish(data, pos)
                if fishClicked != None:
                    fishClicked.onClick(data)

    elif event.type == pygame.MOUSEBUTTONUP:
        data.mouseHeld = False

    elif event.type == pygame.USEREVENT+1: #timer fired every frame
        (data.screenX, data.screenY) = data.player.doMove(data)
        data.bubbleEmitter.update(data)
        for food in data.foods:
            food.update()
        for emitter in data.waterEmitters:
            emitter.update()
        for school in data.schools:
            school.moveAll(data)
        data.oceanBg.update(data)
        updateSpritesScreenPos(data)

    elif event.type == pygame.USEREVENT: #timer fired every second
        for food in data.foods:
            food.secondUpdate(data)
        Food.killEmitters(data)
        WaterEmitter.killEmitters(data)

    data.ui.update(data, event)


def runGame():
    data = Struct()
    data.WIDTH = WIDTH
    data.HEIGHT = HEIGHT

    pygame.init()
    pygame.display.set_caption('Infinite Seas')
    init(data)

    pygame.mixer.init()
    pygame.mixer.music.load('rest.wav')
    pygame.mixer.music.play(-1)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                if data.gameMode == "GAME":
                    gameModeUpdate(data, event)
                elif data.gameMode == "ENCYCLOPEDIA":
                    data.encyclopedia.update(data, event)
                elif data.gameMode == "SPLASH":
                    data.splash.update(data, event)
                elif data.gameMode == "MENU":
                    data.menu.update(data, event)
                elif data.gameMode == "CREATE":
                    data.creator.update(data, event)
                elif data.gameMode == "TUTORIAL":
                    data.tutorial.update(data, event)

        redrawAll(data)

runGame()