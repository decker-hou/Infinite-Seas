import pygame
from button import Button
from Utils import Utils

#Species class keeps information about the species.
class Species(pygame.sprite.Sprite):
    def __init__(self, info):
        pygame.sprite.Sprite.__init__(self)
        self.name = info['name']
        self.scientificName = info['scientific']
        self.imgPath = info['img']
        self.sprite = pygame.image.load(info['img']).convert_alpha()
        self.mask = pygame.mask.from_surface(self.sprite)
        self.bigSprite = pygame.image.load(info['bigImg'])
        self.bigPhoto = pygame.image.load(info['encImg'])
        self.groupSize = info['groupSize']
        self.facts = info['facts']
        self.discovered = False
        self.canInteract = True
        self.factsDiscovered = 0

    def __str__(self):
        return ("Species: name: %s" % self.name)

    def canInteractWith(self):
        return self.canInteract

    def interact(self, data):
        if not self.discovered:
            self.discovered = True
            index = data.encyclopedia.speciesList.index(self)
            data.encyclopedia.speciesDiscovered[index] = 0
        elif self.factsDiscovered < 3:
            self.factsDiscovered += 1
            index = data.encyclopedia.speciesList.index(self)
            data.encyclopedia.speciesDiscovered[index] = self.factsDiscovered

    #sorry about the strings going over the character limit but pygame
    #really doesn't like triple quoted strings
    def drawInfoBox(self, surface):
        if not self.discovered:
            text = "You haven't learned about this species yet! Interact with it to discover more."
            Utils.drawMultilineText(text, surface, 500, 300, Utils.smallFont, 
                                    50, (255,255,255), True)
        else:
            Utils.drawText(self.name, surface, 500, 150, Utils.medFont, 
                           (255,255,255), True)
            Utils.drawText(self.scientificName, surface, 500, 180, 
                           Utils.smallFont, (255,255,255), True)
            Utils.drawText("Facts", surface, 500, 270, Utils.medFont, 
                           (255,255,255), True)
            if self.factsDiscovered == 0:
                text = "You haven't learned any facts about this species yet. Interact with it to learn more."
                Utils.drawMultilineText(text, surface, 500, 300,Utils.smallFont,
                                        50, (255,255,255), True)
            else:
                for i in range(3):
                    if i < self.factsDiscovered:
                        text = self.facts[i]
                    else:
                        text = "???"
                    Utils.drawMultilineText(text, surface, 500, 300+i*100, 
                               Utils.smallFont, 50, (255,255,255), True)

    #draws the individual fact page in the encyclopedia
    def draw(self, surface):
        nameLabel = Utils.bigFont.render(self.name, 1, (0,0,0))
        Utils.blitCenter(nameLabel, surface, (250,50))
        sciLabel = Utils.largishFont.render(self.scientificName, 1, (0,0,0))
        Utils.blitCenter(sciLabel, surface, (250,100))
        Utils.blitCenter(self.bigPhoto, surface, (250, 350))

        for i in range(len(self.facts)):
            if i < self.factsDiscovered:
                text = self.facts[i]
            else:
                text = "???"
            Utils.drawMultilineText(text, surface, 525, 50+i*200, Utils.medFont,
                                    50, (0,0,0))


########################################################################

#An encyclopedia object holds a list of species objects. It's responsible
#for drawing the encyclopedia menu
class Encyclopedia(object):
    unknownSprite = pygame.image.load('assets/question_mark.png')

    #TODO: temp solution for School class, get rid of later
    def getSpeciesObject(name):
        for fishInfo in Encyclopedia.info:
            if fishInfo['name'] == name:
                return Species(fishInfo)
        return None

    info = []
    info.append({'name': 'Sea Goldie',
                'scientific': 'Pseudanthias squamipinnis',
                'img': 'assets/sea_goldie_small.png',
                'bigImg': 'assets/sea_goldie_large.png',
                'encImg': 'assets/sea_goldie_photo.jpg',
                'groupSize': 5,
                'facts': ['Sea goldies from harems consisting of a single male with multiple females.',
                          'When the male of a harem of sea goldies dies, a female will undergo sex change and turn into a male.',
                          'A fish called the Midas blenny mimics the sea goldie\'s color and hides among groups of them.']
                })

    info.append({'name': 'Powder Blue Tang',
                'scientific': 'Acanthurus leucosternon',
                'img': 'assets/powder_tang_small.png',
                'bigImg': 'assets/powder_tang_large.png',
                'encImg': 'assets/powder_tang_photo.jpg',
                'groupSize': 1,
                'facts': ['Powder blue tang can use the "surgeon\'s scalpel", part of their spine near their tail, in self-defence.',
                          'Powder blue tang are difficult to care for in captivity, since they are prone to disease.',
                          'The healthier it is, the more vibrant its blue colouration.']
                })

    info.append({'name': 'Forceps Butterflyfish',
                'scientific': 'Forcipiger flavissimus',
                'img': 'assets/forceps_small.png',
                'bigImg': 'assets/forceps_large.png',
                'encImg': 'assets/forceps_photo.jpg',
                'groupSize': 2,
                'facts': ['The forceps butterflyfish form monogamous pairs for life.',
                          'Forceps butterflyfish pairs are extremely territorial and will chase other pairs from their territory.',
                          'It can produce sound through its body movements, which it uses to advertise its territory.']
                })

    info.append({'name': 'Moorish Idol',
                'scientific': 'Zanclus cornutus',
                'img': 'assets/moorish_idol_small.png',
                'bigImg': 'assets/moorish_idol_large.png',
                'encImg': 'assets/moorish_idol_photo.png',
                'groupSize': 1,
                'facts': ['The Moorish idol got its name from the Moors of Africa, who purportedly believed the fish to be a bringer of happiness.',
                          'The dorsal fin of the Moorish idol forms a long crest called the philomantis extension.',
                          'It is the only surviving species of the family Zanclidae.']
                })

    info.append({'name': 'Ocellaris Clownfish',
                'scientific': 'Amphiprion ocellaris',
                'img': 'assets/clownfish_small.png',
                'bigImg': 'assets/clownfish_large.png',
                'encImg': 'assets/clownfish_photo.jpg',
                'groupSize': 3,
                'facts': ["Clownfish form symbiotic relationships with sea anemones. They\'re protected from the sea anemone\'s sting by a layer of mucus on their body.",
                          'Groups of Ocellaris clownfish form a social hierarchy, with the most dominant members mating most often.',
                          'It is a protandrous hermaphrodite, which means the male can change its gender to female during its life.']
                })

    info.append({'name': 'Royal Angelfish',
                'scientific': 'Pygoplites diacanthus',
                'img': 'assets/royal_small.png',
                'bigImg': 'assets/royal_large.png',
                'encImg': 'assets/royal_photo.jpg',
                'groupSize': 2,
                'facts': ['Roygal angelfish can live up to 14 years in captivity.',
                          'The Regal angelfish mates at dusk or night. The female performs a spiraling dance as she releases her eggs for fertilization.',
                          'Juveniles have a false eye-spot at the base of the dorsal fin that disappears in adulthood.']
                })

    info.append({'name': 'Yellow Tang',
                'scientific': 'Zebrasoma flavescens',
                'img': 'assets/yellow_tang_small.png',
                'bigImg': 'assets/yellow_tang_large.png',
                'encImg': 'assets/yellow_tang_photo.jpg',
                'groupSize': 4,
                'facts': ['Adult yellow tang have 18 upper teeth and 22 lower teeth.',
                          'Its bright yellow color fades slightly at night, and becomes brighter in daytime.',
                          'In the wild, yellow tang provide cleaner services to marine turtles, by removing algal growth from their shells.']
                })

    info.append({'name': 'Red Lionfish',
                'scientific': 'Pterois volitans',
                'img': 'assets/lionfish_small.png',
                'bigImg': 'assets/lionfish_large.png',
                'encImg': 'assets/lionfish_photo.jpg',
                'groupSize': 1,
                'facts': ['Adult yellow tang have 18 upper teeth and 22 lower teeth.',
                          'Its bright yellow color fades slightly at night, and becomes brighter in daytime.',
                          'In the wild, yellow tang provide cleaner services to marine turtles, by removing algal growth from their shells.']
                })

    info.append({'name': 'Common Seahorse',
                'scientific': 'Hippocampus kuda',
                'img': 'assets/seahorse_small.png',
                'bigImg': 'assets/seahorse_large.png',
                'encImg': 'assets/seahorse_photo.png',
                'groupSize': 3,
                'facts': ['Seahorses use their prehensile tails to hold onto coral.',
                          'The male of the species is responsible for brooding the eggs in its ventral pouch.',
                          'Although they are bony fish, they do not have scales, but rather thin skin stretched over a series of bony plates, which are arranged in rings throughout their bodies.']
                })

    info.append({'name': 'Green Sea Turtle',
                'scientific': 'Chelonia mydas',
                'img': 'assets/turtle_small.png',
                'bigImg': 'assets/turtle_large.png',
                'encImg': 'assets/turtle_photo.jpg',
                'groupSize': 1,
                'facts': ['Young green sea turtles are carnivores, but they gradually become herbivores as adults.',
                          'The green sea turtle can sense magnetic fields, they use it for navigation.',
                          'Only 1% of hatchlings reach maturity.']
                })

    info.append({'name': 'Ocean Sunfish',
                'scientific': 'Mola mola',
                'img': 'assets/sunfish_large.png',
                'bigImg': 'assets/sunfish_large.png',
                'encImg': 'assets/sunfish_photo.png',
                'groupSize': 1,
                'facts': ['The ocean sunfish is the heaviest known bony fish in the world. It weighs between 247 and 1000 kg (545–2205 lb).',
                          'Female ocean sunfish produce more eggs than any other known vertebrate, up to 300 million.',
                          'Their closest living relative is the pufferfish.']
                })

    def __init__(self, data):
        self.speciesList = [] #ordered list of species objects
        self.loadSpeciesList()
        #-1 = undiscovered
        #0-3 = 0-3 facts found
        self.speciesDiscovered = [-1]*len(self.speciesList)
        self.page = 0 #what page of the menu you're on
        self.menu = True
        self.speciesIndex = 0 #what species's page we're looking at
        self.numOfSpecies = len(self.speciesList)

        self.paperBg = pygame.image.load("assets/paper_bg.png")
        self.WIDTH = data.WIDTH
        self.HEIGHT = data.HEIGHT

        self.encMenuBtns = set() #misnomer, buttons really
        self.encMenuFishBtns = []
        self.encPageSprites = set()

        self.loadButtons(data)

    def __str__(self):
        return "list: " + str(self.speciesList)

    #call after loading
    #-1 = undiscovered. 0,1,2,3 = facts discovered
    def reloadSpecies(self):
        for i in range(len(self.speciesList)):
            loadInfo = self.speciesDiscovered[i]
            if loadInfo == -1:
                self.speciesList[i].discovered = False
                self.speciesList[i].factsDiscovered = 0
            else:
                self.speciesList[i].discovered = True
                self.speciesList[i].factsDiscovered = loadInfo

    def resetDiscoveries(self):
        self.speciesDiscovered = [-1]*len(self.speciesList)
        self.reloadSpecies()

    def calculateCompletion(self):
        total = len(self.speciesDiscovered) * 4
        points = sum(self.speciesDiscovered) + len(self.speciesDiscovered)
        return int(points / total * 100)

    def loadButtons(self, data):
        def backBtnFn(data): self.menu = True
        backBtn = Button('assets/back_small.png', 20, data.HEIGHT-50, 
                    backBtnFn, group=self.encPageSprites)

        def leftBtnFn(data): 
            self.speciesIndex -= 1
            if self.speciesIndex < 0: 
                self.speciesIndex = len(self.speciesList) - 1
            while not self.speciesList[self.speciesIndex].discovered:
                self.speciesIndex -= 1
                if self.speciesIndex < 0: 
                    self.speciesIndex = len(self.speciesList) - 1
        leftBtn = Button('assets/arrow_left.png', 30, data.HEIGHT//2, 
                         leftBtnFn, True, group=self.encPageSprites)

        def rightBtnFn(data): 
            self.speciesIndex += 1
            if self.speciesIndex >= len(self.speciesList): 
                self.speciesIndex = 0
            while not self.speciesList[self.speciesIndex].discovered:
                self.speciesIndex += 1
                if self.speciesIndex >= len(self.speciesList): 
                    self.speciesIndex = 0
        rightBtn = Button('assets/arrow_right.png', data.WIDTH-35, 
                    data.HEIGHT//2, rightBtnFn, True, group=self.encPageSprites)

        def backBtnFn2(data): data.gameMode = "MENU"
        backBtn2 = Button('assets/back_small.png', 20, data.HEIGHT-50, 
                    backBtnFn2, group=self.encMenuBtns)

        def leftBtnFn2(data): self.page -= 1
        self.leftBtn2 = Button('assets/arrow_left.png', 30, data.HEIGHT//2, 
                    leftBtnFn2, True, group=self.encMenuBtns)

        def rightBtnFn2(data): self.page += 1
        self.rightBtn2 = Button('assets/arrow_right.png', data.WIDTH-35, 
                    data.HEIGHT//2,rightBtnFn2, True, group=self.encMenuBtns)

        def btnFn(this, data):
            index = this.index + self.page*8
            if index < self.numOfSpecies and self.speciesList[index].discovered:
                self.speciesIndex = index
                self.menu = False

        self.fishBtnPos = [(140,140), (360,140), (140,520), (360,520), 
                           (640,140), (860,140), (640,520), (860,520)]
        for i in range(8):
            (x, y) = self.fishBtnPos[i]
            fishBtn = Button('assets/enc_fish_btn.png', x, y, btnFn, True, True) 
            fishBtn.index = i
            self.encMenuBtns.add(fishBtn)
            self.encMenuFishBtns.append(fishBtn)

    def loadSpeciesList(self):
        for fishInfo in Encyclopedia.info:
            name = fishInfo['name']
            specieObj = Species(fishInfo)
            self.speciesList.append(specieObj)

    def updateMenuVisibility(self):
        self.leftBtn2.visible = True if self.page > 0 else False
        self.rightBtn2.visible = (True if ((self.page+1)*8<=self.numOfSpecies)
                                  else False)

    def resetSpeciesInteract(self):
        for species in self.speciesList:
            species.canInteract = True

    def drawInfoPage(self, surface):
        self.speciesList[self.speciesIndex].draw(surface)
        for button in self.encPageSprites:
            button.draw(surface)

    def drawMenuPage(self, surface):
        percent = str(self.calculateCompletion()) + "% complete"
        percentLabel = Utils.largishFont.render(percent, 1, (0,0,0))
        surface.blit(percentLabel, (self.WIDTH-200, self.HEIGHT-40))
        for button in self.encMenuBtns:
            button.draw(surface)
        for i in range(8):
            fishIndex = self.page*8 + i
            if fishIndex < self.numOfSpecies:
                fish = self.speciesList[fishIndex]
                if fish.discovered:
                    sprite = self.speciesList[fishIndex].bigSprite
                else:
                    sprite = Encyclopedia.unknownSprite
                Utils.blitCenter(sprite, surface, self.fishBtnPos[i])


    def draw(self, surface):
        surface.blit(self.paperBg, (0,0))
        if self.menu == True: self.drawMenuPage(surface)
        else: self.drawInfoPage(surface)

    def update(self, data, event):
        self.updateMenuVisibility()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.menu:
                for button in self.encMenuBtns:
                    if button.rect.collidepoint(pos):
                        button.onClick(data)
            else:
                for button in self.encPageSprites:
                    if button.rect.collidepoint(pos):
                        button.onClick(data)
