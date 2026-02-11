import pygame as pg
import sys
from random import *
from os import path
from settings import *
from sprites import *
from utils import *

#the game class that will be instantiaed in order to run the game...
class Game:
    def __init__(self):
        pg.init()
        #setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) #takes in str
        self.clock = pg.time.Clock()

        #starting the game
        self.running = True      
        self.playing = True
        self.game_cooldown = Cooldown(3000)
        self.game_cooldown.start()

    #a method is a function tied to a Class

    def load_data(self):
        self.game_dir = path.dirname(__file__)
        self.map = Map(path.join(self.game_dir, 'level1.txt'))

    def new(self):
        #Starts the game
        #Creating every group, so that we could access all of a certain type of object.
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        self.load_data()

        #Instantiating the objects
        #self.goal = Object(self, 15, 15)
        #self.player = Player(self, 15, 15)
        #self.mob = Mob(self, 15, 15)
        for row,tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    #call class constructor without assigning variable
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        #Telling the game to run
        self.run()

    def run(self):
        while self.running:
            #self.dt is delta time, how much time passsed in real life.
            self.dt = self.clock.tick(FPS) / 1000
            #Looping through everything while it runs.
            self.events()
            self.update()
            self.draw()

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


    def quit(self):
        pass

    def update(self):
        self.all_sprites.update()
        #if self.player.rect.colliderect(self.goal.rect):
            #self.goal.pos = (100, 100)

    def draw(self):
        #BG color
        self.screen.fill(BLUE)

        #Writing texts
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT/1.5)

        #Drawing objects
        self.all_sprites.draw(self.screen)
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