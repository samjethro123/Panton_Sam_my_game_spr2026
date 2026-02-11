import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        #Attributes that the object needs to function, position, velocity, sprite.
        #This will be copied for every object, with a few exceptions.
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    def get_keys(self):

        self.vel = vec(0, 0) #resetting the vector 
        keys = pg.key.get_pressed()

        #WASD pressed -> movement
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        #Diagonal movement moves at the correct speed.
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    def update(self):
        self.get_keys()
        #Syncing the object with the sprite
        self.rect.center = self.pos
        #Vector movement
        self.pos += self.vel * self.game.dt
        for colliders in pg.sprite.spritecollide(self, self.game.all_walls, False):
            print("collided with " + str(colliders))

class Mob(Sprite):
    def __init__(self, game, x, y):
        #Additionally added to all_mobs so that we can access the mobs w/o the player or walls
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    def movement(self):
        pass
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            print(hits)

class Object(Sprite):
    def __init__(self, game, x, y):
        #Similar to mob, added to all_walls
        #Excludes velocity
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass

class Wall(Sprite):
    def __init__(self, game, x, y):
        #Similar to goal, but will stop collision instead
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)

class Coin(Sprite):
    def __init__(self, game, x, y):
        #Similar to goal, but will stop collision instead
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
