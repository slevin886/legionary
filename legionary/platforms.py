import pygame as pg
from .settings import POW_SPAWN_PCT, BOOST_POWER
import random 


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # images = [
        #     self.game.spritesheet.get_image(0, 288, 380, 94),
        #     self.game.spritesheet.get_image(213, 1662, 201, 100),
        # ]
        self.image = pg.Surface((width, height))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        if random.randrange(100) < POW_SPAWN_PCT:
            PowerUp(self.game, self)


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, platform):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.platform = platform
        self.type = "boost" # make this choice? 
        self.image = self.game.sprite_sheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 3

    def update(self):
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 3
        if not self.game.platforms.has(self.platform):
            self.kill()