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

# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 900
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BARREL_OFFSET = vec(30,10)
BULLET_DAMAGE = 10
KICKBACK = 200
GUN_SPREAD = 5

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

# Effects
MUZZLE_FLASHES = ["whitePuff15.png", "whitePuff16.png","whitePuff17.png","whitePuff18.png"]
FLASH_DURATION = 40


# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 5
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png'}
HEALTH_PACK_AMOUNT = 20
