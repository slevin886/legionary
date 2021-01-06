import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, screen_y, screen_x, max_walk=40):
        self._layer = 2
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.walk_frames_l[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_x
        self.rect.bottom = screen_y - 3
        self.left = True
        self.walk_count = 0
        self.max_walk = max_walk
        self.vx = 5
        self.last_update = 0

    def load_images(self):
        self.walk_frames_r = [
            self.game.sprite_sheet_2.get_image(23, 0, 63, 120),
            self.game.sprite_sheet_2.get_image(122, 0, 63, 120)
        ]
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))

        self.walk_frames_l = [pg.transform.flip(frame, True, False) for frame in self.walk_frames_r]

    def update(self):
        now = pg.time.get_ticks()
        if self.walk_count == self.max_walk:
            if now - self.last_update > 200:
                self.last_update = now
                if self.left:
                    self.left = False
                    self.image = self.walk_frames_r[0]
                else:
                    self.left = True
                    self.image = self.walk_frames_l[0]
                self.vx = self.vx * -1
                self.walk_count = 0
        elif now - self.last_update > 150:
            self.last_update = now
            if self.left:
                self.image = self.walk_frames_r[self.walk_count % 2]
            else:
                self.image = self.walk_frames_l[self.walk_count % 2]
            self.rect.centerx += self.vx
            self.walk_count += 1
