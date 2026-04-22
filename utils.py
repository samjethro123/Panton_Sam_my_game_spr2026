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
    def __init__(self):
        self.time = 0
    def tick(self, dt):
        self.time += dt
    def restart(self):
        self.time = 0
    def whatTime(self):
        return int(self.time)
    
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
    def __init__(self, winFrame):
        #winFrame is the name of the txt file describing the win condition
        self.game_dir = path.dirname(__file__)
        self.winmap = []

        with open(winFrame, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

    def checkWin():
        pass

