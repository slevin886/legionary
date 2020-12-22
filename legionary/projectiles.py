import pygame as pg
from legionary.settings import SCREEN_X

class Projectile(pg.sprite.Sprite):
    def __init__(self, game, player):
        self._layer = 2
        self.groups = game.all_sprites, game.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image = self.game.sprite_sheet.get_image(420, 1558, 145, 77)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        if player.left:
            self.vx = -5
            self.rect.right = self.player.rect.left
        else:
            self.vx = 5
            self.rect.left = self.player.rect.right
        self.rect.top = self.player.rect.top
    
    def update(self):
        self.rect.centerx += self.vx
        if self.rect.left > SCREEN_X or self.rect.right < 0:
            self.game.projectile_count -= 1
            self.kill()


# class Projectile:

#     def __init__(self, x, y, radius, direction, color, vel=10):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.direction = direction
#         self.color = color
#         self.vel = vel * direction
    
#     def update(self):
#         pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)