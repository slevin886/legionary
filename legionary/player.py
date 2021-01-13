import os
import pygame as pg
from legionary.projectiles import Projectile
from .settings import *

vec = pg.math.Vector2

class LoadSprites:
    # loading sprite sheet for performance
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width // 2, height // 2))
        return image #0, 0 for corner

class Player(pg.sprite.Sprite):
    def __init__(self, game, acc_rate=0.5, friction=-0.12, gravity=0.5):
        self._layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game # reference to game instance
        # self.image = pg.Surface((30, 40))
        # self.image.fill((0, 255, 0))
        self.load_images()
        self.image = self.walk_frames_r[0]
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.acc_rate = acc_rate
        self.friction = friction
        self.gravity = gravity
        self.rect.center = (SCREEN_X / 2, SCREEN_Y / 2)
        self.pos = vec(SCREEN_X / 2, SCREEN_Y / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.standing = True
        self.walking = False
        self.jumping = False
        self.throwing = False
        self.current_frame = 0
        self.last_update = 0 # space out the frame rate
        self.left = False
        self.right = False

    def load_images(self):
        img_dir = os.path.join(self.game.dir, "pngs/player")
        self.walk_frames_r = [
            self.game.sprite_sheet_2.get_image(259, 0, 60, 98),
            self.game.sprite_sheet_2.get_image(198, 0, 60, 98)
        ]
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))
        self.walk_frames_l = [pg.transform.flip(frame, True, False) for frame in self.walk_frames_r]
        self.throw_images_r = [
            pg.image.load(os.path.join(img_dir, "throw1.png")).convert(),
            pg.image.load(os.path.join(img_dir, "throw2.png")).convert()
        ]
        for frame in self.throw_images_r:
            frame.set_colorkey((0, 0, 0))
        self.throw_images_l = [pg.transform.flip(frame, True, False) for frame in self.throw_images_r]


    def throw(self):
        if not self.throwing:
            self.throwing = True
            self.current_frame = 0
            self.walking = False


    def jump(self, jump_speed=-20):
        # check if on platform
        self.rect.y += 2
        standing = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if standing and not self.jumping:
            self.vel.y = jump_speed
            self.jumping = True
            self.game.jump_sound.play()
    

    def end_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0 and not self.throwing:
            self.walking = True
        else:
            self.walking = False
        # walking animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # standing frames
        if not self.jumping and not self.walking and not self.throwing:
            if now - self.last_update > 250: # ms
                self.last_update = now
                if self.left:
                    self.image = self.walk_frames_l[0]
                else:
                    self.image = self.walk_frames_r[0]
                self.current_frame = 0
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.throwing:
            if now - self.last_update > 250: # ms
                self.last_update = now
                if self.left:
                    self.image = self.throw_images_l[self.current_frame]
                    if self.current_frame == 1:
                        Projectile(self.game, self.rect.midright, -7, 0, "pngs/projectiles/sword.png")
                        self.game.projectile_count += 1
                else:
                    self.image = self.throw_images_r[self.current_frame]
                    if self.current_frame == 1:
                        Projectile(self.game, self.rect.midleft, 7, 0, "pngs/projectiles/sword.png")
                        self.game.projectile_count += 1
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                if self.current_frame == 1:
                    self.throwing = False
                    self.current_frame = 0
                else:
                    self.current_frame = 1


    def update(self):
        self.animate()
        self.acc = vec(0, self.gravity)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = self.acc_rate * -1
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pg.K_RIGHT]:
            self.acc.x = self.acc_rate
            self.left = False
            self.right = True
            self.standing = False
        else:
            self.standing = True
        
        # apply friction
        self.acc.x += self.vel.x * self.friction 
        # motion equations
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += (self.vel + 0.5 * self.acc)
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos
