import pygame as pg
import sys
from random import *
from os import path
from settings import *
from sprites import *
from utils import *

from math import floor

#the game class that will be instantiaed in order to run the game...
class Game:
    def __init__(self):
        print('init!')
        pg.init()
        #setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) #takes in str
        self.clock = pg.time.Clock()

        self.pausetime = 0

        #starting the game
        self.running = True      
        self.playing = True

        self.viewWinCon = False

        self.paused = False

        self.level = 2

        self.mapOrder = [
            'level1.txt',
            'level2.txt',
            'level3.txt',
            'level4.txt',
            'level5.txt'
        ]

        self.winMapOrder = [
            'level1win.txt',
            'level2win.txt',
            'level3win.txt',
            'level4win.txt',
            'level5win.txt'
        ]

    #a method is a function tied to a Class

    def load_data(self):
        #loading map and images
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.wall_img = pg.image.load(path.join(self.img_dir, 'WallSprite.png'))
        self.gun_img = pg.image.load(path.join(self.img_dir, 'floorgun.png'))
        self.boximg = pg.image.load(path.join(self.img_dir, 'box.png'))

        self.map = Map(path.join(self.game_dir, self.mapOrder[self.level-1]), False)
        self.winMap = Map(path.join(self.game_dir, self.winMapOrder[self.level-1]), False)

    def new(self):
        #Starts the game depending on the level

        #Creating every group, so that we could access all of a certain type of object.
        self.theplayer = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.winSprites = pg.sprite.LayeredUpdates()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_boxes = pg.sprite.Group()
        self.all_mags = pg.sprite.Group()
        self.all_floors = pg.sprite.Group()
        self.nonBox = pg.sprite.Group()
        self.all_guns = pg.sprite.Group()

        self.load_data()

        #For the regular map, turns it into a list of lists
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    #call class constructor without assigning variable
                    Wall(self, col, row, False)
                if tile == 'P':
                    self.player = Player(self, col, row, False)
                if tile == 'B':
                    Box(self, col, row, 2, False)
                if tile == 'M':
                    Magnet(self, col, row, 1, False)
                if tile == 'G':
                    Gun(self, col, row, False)

        #For the winCon map
        print(self.winMap.data)

        self.snippets = []
        self.spots = []
        self.tick = 0
        nextLine = 0

        '''
        winMap.data shows snippets of the win condition map, each snippet surrounded by lines with { and }
        Finds the data of the snippet, the two lines following the } describe the top left of where the snippet is
        '''
        for i in range(len(self.winMap.data)):
            if self.winMap.data[i] == '{':
                self.snippet = []
                self.spot = []
                nextLine = i
                while self.winMap.data[nextLine+1] != '}':
                    nextLine += 1
                    self.snippet.append(self.winMap.data[nextLine])\
                    
                self.spot.append(int(self.winMap.data[nextLine+2])-1)
                self.spot.append(int(self.winMap.data[nextLine+3])-1)

                #snippets is a list of lists describing the shape of the snippet
                #spots is a tuple describing the top left of the snippet's position
                #wintick is a number determining which tick the win screen has to be on
                self.snippets.append(self.snippet)
                self.spots.append(self.spot)
            if self.winMap.data[i] == 'wintick':
                self.wintick = int(self.winMap.data[i+1])


        #create mobs that will be drawn when we choose to see the future so that the player can see the win condition

        for i in range(len(self.snippets)):
            for row,tiles in enumerate(self.snippets[i]):
                for col, tile in enumerate(tiles):
                    if tile == '.':
                        Floor(self, col + self.spots[i][0], row + self.spots[i][1])
                    if tile == '1':
                        Wall(self, col + self.spots[i][0], row + self.spots[i][1], True)
                    if tile == 'P':
                        self.player = Player(self, col + self.spots[i][0], row + self.spots[i][1], True)
                    if tile == 'B':
                        Box(self, col + self.spots[i][0], row + self.spots[i][1], 0, True)
                    if tile == 'M':
                        Magnet(self, col + self.spots[i][0], row + self.spots[i][1], 0, True)

        self.WinCheck = WinCheck([self.snippets, self.spots], self)

        self.timer = Timer(self.pausetime)

        #Telling the game to run
        self.run()

    def run(self):
        while self.running:
            #self.dt is delta time, how much time passsed in real life.
            self.dt = self.clock.tick(FPS) / 1000

            #Looping through everything while it runs.

            #If the player is looking at the win condition, nothing should happen.
            if not self.viewWinCon:
                self.update()
                Timer.tick(self.timer, self.paused)
            self.draw()
            self.events()

            #Checks for the win condition
            if floor(Timer.whatTime(self.timer)) == self.wintick:
                print('start wincheck')

                winstate = self.WinCheck.checkWin()

                lostState = True

                while lostState:
                    self.screen.fill(BLACK)
                    self.draw_text(str(winstate), 100, YELLOW, WIDTH/2, HEIGHT/2)
                    pg.display.flip()




                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            if self.playing:
                                self.playing = False
                            self.running = False
                        if event.type == pg.KEYDOWN:
                            self.player.get_keys()
                            keys = pg.key.get_pressed()
                    
                            if keys[pg.K_r]:
                                if winstate == True:
                                    self.level+=1
                                lostState = False
                                self.pausetime = Timer.reset(self.timer) - self.pausetime
                                self.new()

    def events(self):
        #events with peripheral devices
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #if event.type == pg.MOUSEMOTION:
                #print(event.pos)
            if event.type == pg.KEYDOWN:
                self.player.get_keys()

                keys = pg.key.get_pressed()

                if keys[pg.K_m]:
                    self.viewWinCon = not self.viewWinCon
                    print(self.viewWinCon)
        
                if keys[pg.K_n]:
                    WinCheck.checkWin(self.WinCheck)
                    print('n press')

                if keys[pg.K_p]:
                    print(self.paused)

                    if self.paused == True:
                        Timer.endpause(self.timer)
                    else:
                        Timer.pause(self.timer)
                    self.paused = not self.paused
    


    def quit(self):
        pass

    def update(self):

        '''
        Order of movements:

        X direction movement
         Player moves
         Boxes collide with everything
         Player collide with walls and boxes

        Y direction movement
         Player moves
         Boxes collide with everything
         Player collide with walls and boxes

        Draw sprites
        '''

        self.player.update('movementX')
        self.all_boxes.update('playerX')
        self.all_boxes.update('boxX')
        self.all_boxes.update('wallX')
        self.all_boxes.update("boxY")
        self.all_boxes.update('magX')
        self.player.update('collisionsX')

        self.player.update('movementY')
        self.all_boxes.update('playerY')
        self.all_boxes.update('boxY')
        self.all_boxes.update('wallY')
        self.all_boxes.update('boxY')
        self.all_boxes.update('magY')
        self.player.update('collisionsY')

        self.all_sprites.update('updateSprite')

    def draw(self):
        #BG color
        if not self.viewWinCon:

            self.screen.fill(BLUE)

            #Writing texts
            self.draw_text(str(floor(Timer.whatTime(self.timer))), 50, WHITE, WIDTH-200, HEIGHT-200)

            #Drawing objects
            self.all_sprites.draw(self.screen)
            
            pg.display.flip()

        else:
            self.screen.fill(BLACK)

            #Drawing objects on the wincon map
            self.winSprites.draw(self.screen)

            self.draw_text(str(self.wintick), 50, YELLOW, WIDTH-200, HEIGHT-200)
            pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    g = Game()

while g.running:
    g.new()

pg.quit()