
from unittest import case

import pygame as pg
from pygame import sprite
from pygame.sprite import Sprite
from settings import *
from os import path
from utils import *

vec = pg.math.Vector2

'''
def futureMovement(center, centerVel, collider):

    testRect = center.hit_rect.copy()


    testRect.pos = center.pos + centerVel * center.game.dt
    
    if testRect.colliderect(collider):
        return True
    return False
'''
#Returns a bool depending on whether two objects are colliding
def collide_hit_rect(one, two):
    if one.hit_rect != None and two.hit_rect != None:
        return one.hit_rect.colliderect(two.hit_rect)
    elif one.hit_rect != None:
        return one.hit_rect.colliderect(two.rect)
    elif two.hit_rect != None:
        return one.rect.colliderect(two.hit_rect)
    else:
        return one.rect.colliderect(two.rect)


def collide_walls(sprite, spriteRect, group, dir):
    #Returns direction of collision, collider, distance between the centers in the direction stated

    #Polymorphed to support other collisions

    #Stops movement in x direction
    if dir == 'x':
        #Identifies the collider 
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        #print(hits)
        if hits:
            #If the collider is to the right
            if hits[0].rect.centerx > spriteRect.centerx:
                return "right", hits[0], hits[0].rect.centerx - spriteRect.centerx
            
            #If the collider is to the left
            if hits[0].rect.centerx < spriteRect.centerx:
                return "left", hits[0], spriteRect.centerx - hits[0].rect.centerx
            
    #Stop movement in y direction
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            #If the collider is below it
            if hits[0].rect.centery > spriteRect.centery:
                return "down", hits[0], hits[0].rect.centery - spriteRect.centery
            
            #If the collider is on top of it
            if hits[0].rect.centery < spriteRect.centery:
                return "up", hits[0], spriteRect.centery - hits[0].rect.centery

    return None, None, None


def collide_box(player, boxes, dir):
    collided = collide_walls(player, boxes, dir)
    if collided[0] != None:
        if dir == 'x':
            if collided == "right":
                futurePoint = collided[1].topright + PLAYER_SPEED * player.game.dt
                


class Player(Sprite):
    def __init__(self, game, x, y):
        #Adding to sprites -> draw
        self.groups = game.all_sprites, game.theplayer
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

        '''
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
        '''

    '''
    Flow of player movement:
    1. Detect if player has pressed a key, then move the hitbox if so
    2. Check if hitbox collides with wall, if so move player to edge of wall
    3. Draw the player
    '''

    def update(self, updateType):
        if updateType == "movementX":
            #Moves hitbox depending on keys x direction
            self.get_keys()
            self.pos.x += self.vel.x * self.game.dt
            self.hit_rect.centerx = self.pos.x

        
        if updateType == "movementY":
            #Moves hitbox depending on keys y direction
            self.get_keys()
            self.pos.y += self.vel.y * self.game.dt
            self.hit_rect.centery = self.pos.y
    
        
        if updateType == "collisionsY":
            #Moves hitbox depending on walls in y direction
            pushDirY = collide_walls(self, self.hit_rect, self.game.all_walls, 'y')

            #If collision in y direction, move player to correct edge of wall and stop y movement
            if pushDirY[0] != None:
                if pushDirY[0] == "down":
                    self.pos.y = pushDirY[1].rect.top - self.hit_rect.height / 2
                if pushDirY[0] == "up":
                    self.pos.y = pushDirY[1].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y
                
        if updateType == "collisionsX":
            #Moves hitbox depending on walls in x direction
            self.hit_rect.centerx = self.pos.x
            pushDirX = collide_walls(self, self.hit_rect, self.game.all_walls, 'x')

            #If collision in x direction, move player to correct edge of wall and stop x movement 
            if pushDirX[0] != None:
                if pushDirX[0] == "right":
                    self.pos.x = pushDirX[1].rect.left - self.hit_rect.width / 2
                if pushDirX[0] == "left":
                    self.pos.x = pushDirX[1].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x

        if updateType == "updateSprite":
            self.rect.center = self.pos
        
            
class Box(Sprite):
    def __init__(self, game, x, y, _layer):
        self._layer = _layer
        self.game = game

        #all_boxes is for anything that could be pushed
        self.groups = game.all_boxes, game.all_walls, game.all_sprites

        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)

        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = pg.Rect(0,0,TILESIZE,TILESIZE)

        self.rect.center = self.pos
        
    def update(self, updateType): 
        if updateType == "collisionsX":

            #Player Box collision
            pushingDirX = collide_walls(self, self.hit_rect, self.game.theplayer, "x")

            if pushingDirX[0] != None:
                if pushingDirX[0] == "right":
                    self.vel.x = -PLAYER_SPEED
                elif pushingDirX[0] == "left":
                    self.vel.x = PLAYER_SPEED

            self.pos.x += self.vel.x * self.game.dt
            self.vel.x = 0
            self.hit_rect.centerx = self.pos.x

            #Box Wall collision
            pushDirX = collide_walls(self, self.hit_rect, self.game.nonBox, 'x')
            if pushDirX[0] != None:
                if pushDirX[0] == "right":
                    self.pos.x = pushDirX[1].rect.left - self.hit_rect.width / 2
                if pushDirX[0] == "left":
                    self.pos.x = pushDirX[1].rect.right + self.hit_rect.width / 2
                self.vel.x = 0

            self.hit_rect.centerx = self.pos.x

            #Box Magnet collision
            magDirX = collide_walls(self, self.hit_rect, self.game.all_mags, 'x')
            if magDirX[2] != 0 and magDirX[0] != None:
                if magDirX[2] > MAG_STRENGTH:
                    if magDirX[0] == "right":
                        self.pos.x += MAG_STRENGTH
                    if magDirX[0] == "left":
                        self.pos.x += -MAG_STRENGTH
                else:
                    self.pos.x = magDirX[1].rect.centerx
                self.hit_rect.centerx = self.pos.x
        
        if updateType == 'collisionsY':

            #Player Box collision
            pushingDirY = collide_walls(self, self.hit_rect, self.game.theplayer, "y")

            if pushingDirY[0] != None:
                if pushingDirY[0] == "down":
                    self.vel.y = -PLAYER_SPEED
                elif pushingDirY[0] == "up":
                    self.vel.y = PLAYER_SPEED
            
            self.pos.y += self.vel.y * self.game.dt
            self.vel.y = 0
            self.hit_rect.centery = self.pos.y

            #Box Wall collision
            pushDirY = collide_walls(self, self.hit_rect, self.game.nonBox, 'y')
            if pushDirY[0] != None:
                if pushDirY[0] == "down":
                    self.pos.y = pushDirY[1].rect.top - self.hit_rect.height / 2
                if pushDirY[0] == "up":
                    self.pos.y = pushDirY[1].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0

            self.hit_rect.centery = self.pos.y

            #Box Magnet detection
            magDirY = collide_walls(self, self.hit_rect, self.game.all_mags, 'y')
            if magDirY[2] != 0 and magDirY[0] != None:
                if magDirY[2] > MAG_STRENGTH:
                    if magDirY[0] == "down":
                        self.pos.y += MAG_STRENGTH
                    if magDirY[0] == "up":
                        self.pos.y += -MAG_STRENGTH
                else:
                    self.pos.y = magDirY[1].rect.centery
                self.hit_rect.centery = self.pos.y

        if updateType == 'updateSprite':
            self.rect.center = self.pos
            
class Magnet(Sprite):
    def __init__(self, game, x, y, _layer):

        self._layer = _layer
        self.groups = game.all_sprites, game.all_mags
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(0,0,TILESIZE,TILESIZE)
        self.hit_rect.center = self.pos

        print("mag cent" + str(self.pos))

    def update(self, updateType):
        pass

#not built upon yet
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
    def update(self, updateType):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            print(hits)



        #print(self.game.theplayer)



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
    def update(self, updateType):
        pass

class Wall(Sprite):
    def __init__(self, game, x, y):
        #Similar to object, but will stop collision instead
        self.groups = game.all_sprites, game.all_walls, game.nonBox
        Sprite.__init__(self, self.groups)
        self.game = game

        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = None
    def update(self, updateType):
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
    def update(self, updateType):
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
    def update(self, updateType):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            print(hits)

