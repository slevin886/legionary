import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
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
