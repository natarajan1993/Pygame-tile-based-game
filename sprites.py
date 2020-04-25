import pygame as pg
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        # Get all collisions between player and walls
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

        if hits:
            if sprite.vel.x > 0:  # Sprite is moving right when it collided with wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2

            if sprite.vel.x < 0:  # Sprite is moving left when it collided with wall
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

        if hits:
            if sprite.vel.y > 0:  # Sprite is moving down when it collided with wall
                # This will allow the player to slide on the other direction
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                # if he was moving in X plane, slide in y plane and vice-versa

            if sprite.vel.y < 0:  # Sprite is moving up when it collided with wall
                # Divide by 2 because the player sprite is calculated at the center of the image
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0  # 0 deg is pointing to right

    def get_keys(self):
        self.vel = vec(0, 0)
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

    

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        # % 360 keeps rotation between 0 and 360 deg
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(
            self.game.player_img, self.rot)  # Rotate the player sprite
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0,0)
        self.acc = vec(0,0) # Acceleration of turning

        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0)) # Make zombie point to player with vector subtraction
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 # v = ut + 1/2 at^2

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center