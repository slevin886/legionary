import pygame as pg
from .settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, acc_rate=0.5, friction=-0.12):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.acc_rate = acc_rate
        self.friction = friction
        self.rect.center = (SCREEN_X / 2, SCREEN_Y / 2)
        self.pos = vec(SCREEN_X / 2, SCREEN_Y / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.standing = True
        self.left = False
        self.right = False

    def update(self):
        self.acc = vec(0, 0.5)
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
        self.pos += (self.vel + 0.5 * self.acc)
        # instituting wrap around
        if self.pos.x > SCREEN_X:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_X
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