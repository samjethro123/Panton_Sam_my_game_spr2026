import pygame as pg

#Initializing Variables
WIDTH = 1024
HEIGHT = 800
FPS = 60
TITLE = "My cool game..."
TILESIZE = 32

#Character Attributes
PLAYER_SPEED = 280
PLAYER_HIT_RECT = pg.Rect(0,0,TILESIZE,TILESIZE)

#Object Settings
MAG_STRENGTH = 1

#Framerate for animations
IDLE_RATE = 1000
WALKING_RATE = 1

TICKLENGTH = 1000

#Hidden mobs

#Color Values
#tuples storing rbg values
BLUE = (0, 0, 255) #bg
WHITE = (255, 255, 255) #player
BLACK = (0, 0, 0) #mob
RED = (255, 0, 0) #goal
GREEN = (0, 255, 0) #wall
YELLOW = (255, 122, 9) #coin