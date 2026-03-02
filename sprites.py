import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random

vec = pg.math.Vector2

#Returns a bool depending on whether two objects are colliding
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

#Checks for x/y collision and sets position depending on direction
def collide_walls(sprite, group, dir):
    #Stops movement in x direction
    if dir == 'x':
        #Identifies the collider 
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            #If the collider is to the right, put the object on its left.
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2

            #If the collider is to the left, put the object on the right
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2

            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    #Stop movement in y direction
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            #If the collider is below it, put the object on top.
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.width / 2

            #If the collider is on top of it, put the object on the bottom
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.width / 2

            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

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
        self.hit_rect = PLAYER_HIT_RECT
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
    
        #Diagonal movement correction
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    def update(self):
        self.get_keys()
        #Syncing the object with the sprite
        self.rect.center = self.pos
        #Vector movement
        self.pos += self.vel * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_walls(self, self.game.all_walls, 'y')
        self.hit_rect.centerx = self.pos.x
        collide_walls(self, self.game.all_walls, 'x')
        #self.

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
        #Similar to object, but will stop collision instead
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)

class Coin(Sprite):
    def __init__(self, game, x, y):
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

