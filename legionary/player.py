import pygame as pg
from .settings import *

vec = pg.math.Vector2

class LoadSprites:
    # loading sprite sheet for performance
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image #0, 0 for corner

class Player(pg.sprite.Sprite):
    def __init__(self, game, acc_rate=0.5, friction=-0.12, gravity=0.5):
        pg.sprite.Sprite.__init__(self)
        self.game = game # reference to game instance
        # self.image = pg.Surface((30, 40))
        # self.image.fill((0, 255, 0))
        self.load_images()
        self.image = self.standing_frames[0]
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
        self.current_frame = 0
        self.last_update = 0 # space out the frame rate
        self.left = False
        self.right = False

    def load_images(self):
        # assumes sprite sheet
        self.standing_frames = [
            self.game.sprite_sheet.get_image(614, 1063, 120, 191),
            self.game.sprite_sheet.get_image(690, 406, 120, 201)
        ]
        for frame in self.standing_frames:
            frame.set_colorkey((0, 0, 0))
        self.walk_frames_r = [
            self.game.sprite_sheet.get_image(678, 860, 120, 201),
            self.game.sprite_sheet.get_image(692, 1458, 120, 207)
        ]
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))

        self.walk_frames_l = [pg.transform.flip(frame, True, False) for frame in self.walk_frames_r]
        self.jump_frame = self.game.sprite_sheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey((0, 0, 0))

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
        if self.vel.x != 0:
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
        if not self.jumping and not self.walking:
            if now - self.last_update > 250: # ms
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

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
            self.walk_count = 0
        
        # apply friction
        self.acc.x += self.vel.x * self.friction 
        # motion equations
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += (self.vel + 0.5 * self.acc)
        # instituting wrap around
        # if self.pos.x > SCREEN_X:
        #     self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos





# class Player:

#     def __init__(self, x, y, width, height, walk_images, velx=5, vely=8):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.velx = velx
#         self.vely = vely
#         self.left = False
#         self.right = False
#         self.jump = False
#         self.jump_count = 10
#         self.walk_count = 0
#         self.walk_right = walk_images
#         self.walk_left = [pygame.transform.flip(i, True, False) for i in walk_images]
#         # self.standing_image = walk_right[0]
#         self.standing = True
#         # self.hitbox = (self.x + 17, self.y + 11, 29, 54)
#         self.rect = pygame.Rect(self.x + 17, self.y + 11, 29, 54)
#         self.health = 10


#     def update(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_SPACE] and reload_timer == 0:
#             reload_timer = 1
#             if self.left:
#                 bullet_right = -1
#             else: 
#                 bullet_right = 1
#             if len(bullets) < 5:
#                 bullets.append(
#                     Projectile(
#                         round(self.x + self.width // 2), 
#                         round(self.y + self.height // 2),
#                         6,
#                         bullet_right, 
#                         (0, 0, 0)
#                         )
#                     )
#         if keys[pygame.K_LEFT] and self.x > self.velx:
#             self.x -= self.velx
#             self.rect.x -= self.velx
#             self.left = True
#             self.right = False
#             self.standing = False
#         elif keys[pygame.K_RIGHT] and self.x < (SCREEN_X - self.width - self.velx):
#             self.x += self.velx
#             self.rect.x -= self.velx
#             self.left = False
#             self.right = True
#             self.standing = False
#         else:
#             self.standing = True
#             self.walk_count = 0
#         if not self.jump:
#             if keys[pygame.K_UP]:
#                 self.jump = True
#                 self.standing = True
#                 self.walk_count = 0
#         else:
#             self.standing = True
#             if self.jump_count >= -10:
#                 # Change next line to vely?
#                 self.y -= (abs(self.jump_count) * self.jump_count) * 0.5
#                 self.jump_count -= 1
#             else:
#                 self.jump = False
#                 self.jump_count = 10

#     def draw(self, screen):
#         if self.walk_count + 1 >= 27:
#             self.walk_count = 0
#         if not self.standing:
#             if self.left:
#                 screen.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
#                 self.walk_count += 1
#             elif self.right:
#                 screen.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
#                 self.walk_count += 1
#         else:
#             if self.left:
#                 screen.blit(self.walk_left[0], (self.x, self.y))
#             else:
#                 screen.blit(self.walk_right[0], (self.x, self.y))
#         if self.left: # correct for image turninig left:
#             self.hitbox = (self.x + 55, self.y + 3, 35, 95)
#             self.rect = pygame.Rect(self.x + 55, self.y + 3, 35, 95)
#         else:
#             self.hitbox = (self.x + 25, self.y + 3, 35, 95)
#             self.rect = pygame.Rect(self.x + 25, self.y + 3, 35, 95)
#         pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
#     def hit(self):
#         self.health -= 1
#         return 1