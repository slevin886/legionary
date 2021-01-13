import pygame as pg
import os
from legionary.settings import SCREEN_X, SCREEN_Y

vec = pg.math.Vector2

class Projectile(pg.sprite.Sprite):
    def __init__(self, game, tl_xy_coord: tuple, velx: int, vely: int, img_path: str):
        self._layer = 2
        self.groups = game.all_sprites, game.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img_path = os.path.join(self.game.dir, img_path)
        self.load_image(img_path, velx)
        self.rect = self.image.get_rect()
        self.vel = vec(velx, vely)
        if velx < 0:
            self.rect.top = tl_xy_coord[1]
            self.rect.right = tl_xy_coord[0] - 25
        else:
            self.rect.top = tl_xy_coord[1]
            self.rect.left = tl_xy_coord[0] + 25

    def load_image(self, img_path, velx):
        self.image = pg.image.load(self.img_path).convert()
        if velx < 0:
            self.image = pg.transform.flip(self.image, True, False)
        self.image.set_colorkey((0, 0, 0))

    def update(self):
        self.rect.midleft += self.vel
        if (self.rect.left > SCREEN_X or self.rect.right < 0 or self.rect.bottom > SCREEN_Y):
            self.game.projectile_count -= 1
            self.kill()
