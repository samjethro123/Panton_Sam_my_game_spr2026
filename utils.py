import pygame as pg
from settings import *
from os import path

class Map:
    def __init__(self, filename, isWinMap):
        #Creating a list to represent the map
        if not isWinMap:
            self.data = []

            #Open a specific tile and close it with "with"
            with open(filename, 'rt') as f:
                for line in f:
                    self.data.append(line.strip())

            self.tilewidth = len(self.data[0])
            self.tileheight = len(self.data)
            self.width = self.tilewidth * TILESIZE
            self.height = self.tileheight * TILESIZE

#this class creates a countdown
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        #the property of time until cooldown
        self.time = time
    def start(self):
        #how long since Cooldown was initialized
        self.start_time = pg.time.get_ticks()
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        if current_time - self.start_time >= self.time:
            return True
        return False
    
class Timer:
    def __init__(self, pausetime):
        self.time = 0
        self.pausestart = 0
        self.pausetime = pausetime

    def reset(self):
        self.pausetime += pg.time.get_ticks()
        return self.pausetime

    def tick(self, paused):
        if not paused:
            self.time = pg.time.get_ticks()-self.pausetime
            print(self.pausetime)
            print(self.time)

    def pause(self):
        self.pausestart = pg.time.get_ticks()
        self.time = 0
    
    def endpause(self):
        self.pausetime += pg.time.get_ticks()-self.pausestart

    def whatTime(self):
        return int(self.time) / TICKLENGTH
    
    
class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        #print("returning image")
        return image

class WinCheck:
    def __init__(self, winFrame, game):
        self.game = game

        '''
        Winframe
            Snippets
                Snippet
                    Row
                        Column
            Spots
                Spot
                    X spot
                    Y spot
        '''
        self.winFrame = winFrame

    def checkWin(self):

        walls = iter(self.game.all_walls)
        boxes = iter(self.game.all_boxes)
        magnets = iter(self.game.all_mags)
        player = iter(self.game.theplayer)
        floors = iter(self.game.all_floors)
        
        for snippet in self.winFrame[0]:
            for row in snippet:
                for column in row:
                    if column == '.':
                        pass
                    if column == 'B':
                        for box in self.game.all_boxes:
                            nextBox = next(boxes)
                            winPos = pg.Vector2(self.winFrame[1][self.winFrame[0].index(snippet)][0]*TILESIZE+snippet.index(row)*TILESIZE, self.winFrame[1][self.winFrame[0].index(snippet)][1]*TILESIZE+row.index(column)*TILESIZE)

                            if nextBox.pos == winPos:
                                return True
                            else:
                                print('not yet!')

                    if column == 'M':
                        pass
                    if column == 'P':
                        pass

        return False




