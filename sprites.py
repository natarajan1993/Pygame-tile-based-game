import pygame as pg
import pytweening as tween
from random import uniform, choice, randint
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        # Get all collisions between player and walls
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:   # Sprite is moving right when it collided with wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2

            if hits[0].rect.centerx < sprite.hit_rect.centerx:  # Sprite is moving left when it collided with wall
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

        if hits:
            if  hits[0].rect.centery > sprite.hit_rect.centery:  # Sprite is moving down when it collided with wall
                # This will allow the player to slide on the other direction
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                # if he was moving in X plane, slide in y plane and vice-versa

            if hits[0].rect.centery < sprite.hit_rect.centery:  # Sprite is moving up when it collided with wall
                # Divide by 2 because the player sprite is calculated at the center of the image
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec( pos )
        self.rect.center = self.pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = direction.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) 
        self.rot = 0  # 0 deg is pointing to right
        self.last_shot = 0
        self.health = PLAYER_HEALTH

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
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                direction = vec(1,0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, direction)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)

                MuzzleFlash(self.game, pos)

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

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0) # Acceleration of turning

        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.speed = choice(MOB_SPEEDS)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()


    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0)) # Make zombie point to player with vector subtraction
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 # v = ut + 1/2 at^2

        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED

        width = int(self.rect.width * self.health / MOB_HEALTH)

        self.health_bar = pg.Rect(0,0,width,7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20,50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, item_type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[item_type] 
        self.rect = self.image.get_rect()
        self.pos = pos
        self.item_type = item_type
        self.rect.center = pos 
        self.tween = tween.easeInOutSine
        self.step = 0
        self.direction = 1

    def update(self):
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.direction
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.direction *= -1
