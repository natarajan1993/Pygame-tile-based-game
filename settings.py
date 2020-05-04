import pygame as pg

vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'element_green_square.png'

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {
                        'bullet_speed': 500,
                        'bullet_lifetime': 1000,
                        'rate': 250,
                        'kickback': 200,
                        'spread': 5,
                        'damage': 10,
                        'bullet_size':'lg',
                        'bullet_count':1
                    }
WEAPONS['shotgun'] = {
                        'bullet_speed': 400,
                        'bullet_lifetime': 500,
                        'rate': 900,
                        'kickback': 300,
                        'spread': 20,
                        'damage': 5,
                        'bullet_size':'sm',
                        'bullet_count':12
                    }
# BULLET_SPEED = 900
# BULLET_LIFETIME = 1000
# BULLET_RATE = 150
BARREL_OFFSET = vec(30,10)
# BULLET_DAMAGE = 10
# KICKBACK = 200
# GUN_SPREAD = 5

# Player settings
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 250 #degrees/sec
PLAYER_IMAGE = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
PLAYER_HEALTH = 500

# Mob Settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [ 250 , 150, 200, 75, 100]
MOB_HIT_RECT = pg.Rect(0,0,30,30)
MOB_HEALTH = 100
MOB_DAMAGE = 5
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50 # pixels
DETECT_RADIUS = 400
# Effects
MUZZLE_FLASHES = ["whitePuff15.png", "whitePuff16.png","whitePuff17.png","whitePuff18.png"]
FLASH_DURATION = 40
SPLAT = 'splat green.png'
DAMAGE_ALPHA = [i for i in range(0,255,25)]

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 5
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
                'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 20
BOB_SPEED = 0.6


# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav','pain/9.wav','pain/10.wav','pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav','brains3.wav','zombie-roar-1.wav','zombie-roar-2.wav','zombie-roar-3.wav','zombie-roar-5.wav','zombie-roar-6.wav',
                        'zombie-roar-6.wav','zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol':['pistol.wav'], 'shotgun':['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start':'level_start.wav', 'health_up':'health_pack.wav', 'gun_pickup':'gun_pickup.wav'}
