import pygame as pg
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rot = 0 # 0 deg is pointing to right

    
    def get_keys(self):
        self.vel = vec(0,0)
        self.rot_speed = 0
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2, 0).rotate(-self.rot)

        
        # if self.vel.x != 0 and self.vel.y != 0: # To make sure the diagonal doesn't move faster
        #     self.vel *= 0.7071 # 0.7071 = 1/sqrt(2)

    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect) #Get all collisions between player and walls

            if hits:
                if self.vel.x > 0: # Sprite is moving right when it collided with wall
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                
                if self.vel.x < 0: # Sprite is moving left when it collided with wall
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)

            if hits:
                if self.vel.y > 0: # Sprite is moving down when it collided with wall
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2 # This will allow the player to slide on the other direction
                    # if he was moving in X plane, slide in y plane and vice-versa
                
                if self.vel.y < 0: # Sprite is moving up when it collided with wall
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2 # Divide by 2 because the player sprite is calculated at the center of the image
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 # % 360 keeps rotation between 0 and 360 deg
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')

        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')

        self.rect.center = self.hit_rect.center

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE