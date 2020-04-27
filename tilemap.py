import pygame as pg
from settings import *
import pytmx


def collide_hit_rect(sprite_one, sprite_two):
    return sprite_one.hit_rect.colliderect(sprite_two.rect)

class Map:
    def __init__(self, filename):
        """Load map data from a text file and append it to the map data text file"""
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip()) # Removes \n at the end of the line

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)

        self.width = self.tilewidth * TILESIZE # Pixel size
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface



class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        #Limit scrolling to map size
        x = min(0,x) # left
        y = min(0,y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom


        self.camera = pg.Rect(x, y, self.width, self.height)
