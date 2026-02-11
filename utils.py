import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        #Creating a list to represent the map
        self.data = []

        #Open a specific tile and close it with "with"
        with open(filename, 'rt') as f:
            for line in f:
                print("PLEASE")
                self.data.append(line.strip())
                print("something added")
        print(self.data)
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
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False