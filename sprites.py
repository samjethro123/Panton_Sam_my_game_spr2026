
from unittest import case

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from os import path
from utils import *

vec = pg.math.Vector2

#Returns a bool depending on whether two objects are colliding
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

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

#Checks for x/y collision
def collideDir(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        #Distance of the main sprite to the detected collider, centered on the collider
        distanceRight = sprite.hit_rect.centerx - hits[0].rect.centerx
        distanceDown = sprite.hit_rect.centery - hits[0].rect.centery
        distanceLeft = hits[0].rect.centerx - sprite.hit_rect.centerx
        distanceUp = hits[0].rect.centery - sprite.hit_rect.centery

        if distanceRight > distanceLeft and distanceRight > distanceDown and distanceRight > distanceUp:
            return "left", hits[0]
        if distanceDown > distanceRight and distanceDown > distanceLeft and distanceDown > distanceUp:
            return "up", hits[0]
        if distanceLeft > distanceRight and distanceLeft > distanceDown and distanceLeft > distanceUp:
            return "right", hits[0]
        if distanceUp > distanceRight and distanceUp > distanceDown and distanceUp > distanceLeft:
            return "down", hits[0]
    return "none", "none"


def collide_walls(sprite, group):
    dirCardinal,wall = collideDir(sprite, group)
    match dirCardinal:
        case "right":
            sprite.pos.x = wall.rect.left - sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        case "left":
            sprite.pos.x = wall.rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        case "down":
            sprite.pos.y = wall.rect.top - sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
        case "up":
            sprite.pos.y = wall.rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(Sprite):
    def __init__(self, game, x, y):
        #Adding to sprites -> draw
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game

        #loading animated attributes
        self.standingsheet = SpriteSheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.walkingsheet = SpriteSheet(path.join(self.game.img_dir, "player_direction.png"))
        self.standing_frames = self.load_images(self.standingsheet, 2)
        self.walking_frames = self.load_images(self.walkingsheet, 4)

        #Player/Sprite attributes
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT

        #Attributes for animation
        self.jumping = False
        self.walking = False
        self.last_update = -1000
        self.current_frame = 0

    def get_keys(self):
        self.vel = vec(0, 0) #resetting the vector 
        keys = pg.key.get_pressed()

        if keys[pg.K_f]:
            print("i fired")
            p = Projectile(self.game, self.rect.x, self.rect.y)

        #WASD pressed -> movement, also sets self.walking
        #0 = up, 1 = left, 2 = right, 3 = down
        if keys[pg.K_a]:
            #Left
            self.vel.x = -PLAYER_SPEED
            self.walking = True
            self.direction = 1
        if keys[pg.K_w]:
            #Up
            self.vel.y = -PLAYER_SPEED
            self.walking = True
            self.direction = 0
        if keys[pg.K_s]:
            #Down
            self.vel.y = PLAYER_SPEED
            self.walking = True
            self.direction = 3
        if keys[pg.K_d]:
            #Right
            self.vel.x = PLAYER_SPEED
            self.walking = True
            self.direction = 2

        if not keys[pg.K_a] and not keys[pg.K_w] and not keys[pg.K_s] and not keys[pg.K_d]:
            self.walking = False

        #Diagonal movement correction
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def load_images(self, sprite, numframes):
        #Adds each frame as an image to a list
        frames = []
        for frame in range(numframes):
            frames.append(sprite.get_image(TILESIZE*frame,0,TILESIZE,TILESIZE))
        #Makes transparent pixels transparent
        for frame in frames:
            frame.set_colorkey(BLACK)
        return frames

    def animate(self, idlerate, walkingrate):
        now = pg.time.get_ticks()

        #Standing animation
        if not self.jumping and not self.walking:
            if now - self.last_update > idlerate:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #Wakling animation
        elif self.walking and not self.jumping:
            if now - self.last_update > walkingrate:
                self.last_update = now
                self.current_frame = self.direction
                bottom = self.rect.bottom
                self.image = self.walking_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def update(self):
        #changes self.vel direction depending on key pressed
        self.get_keys()

        #updates to next frame depending on state, only every 1000 ticks
        self.animate(IDLE_RATE, WALKING_RATE)

        #Syncing the object with the sprite
        self.rect.center = self.pos 

        #Vector movement
        self.pos += self.vel * self.game.dt
        
        self.hit_rect.centery = self.pos.y
        self.hit_rect.centerx = self.pos.x

        self.hit_rect.centery = self.pos.y
        collide_walls(self, self.game.all_walls, 'y')
        self.hit_rect.centerx = self.pos.x
        collide_walls(self, self.game.all_walls, 'x')
        #collide_walls(self, self.game.all_walls)

        for colliders in pg.sprite.spritecollide(self, self.game.all_walls, False):
            print("collided with " + str(colliders))



class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y)
    def movement(self):
        pass
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            print(hits)



class Box(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_boxes
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT




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

