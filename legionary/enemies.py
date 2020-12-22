import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, screen_y, screen_x, max_walk=40):
        self._layer = 2
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_left = self.game.sprite_sheet.get_image(566, 510, 122, 139)
        self.image_left.set_colorkey((0, 0, 0))
        self.image_right = self.game.sprite_sheet.get_image(568, 1534, 122, 135)
        self.image_right.set_colorkey((0, 0, 0))
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_x
        self.rect.bottom = screen_y - 3
        self.left = True
        self.walk_count = 0
        self.max_walk = max_walk
        self.sleep_count = 0
        self.vx = 3

    def update(self):
        if self.walk_count == self.max_walk:
            if self.left:
                self.left = False
                self.image = self.image_right
            else:
                self.left = True
                self.image = self.image_left
            self.vx = self.vx * -1
            self.walk_count = 0
            self.sleep_count = 20
        else:
            if self.sleep_count == 0:
                self.walk_count += 1
                self.rect.centerx += self.vx
            else:
                self.sleep_count -= 1


# class Enemy:
#     def __init__(self, x, y, width, height, end, walk_images, vel=5):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.vel = vel
#         self.end = end
#         self.walk_count = 0
#         self.path a= [self.x, self.end]
#         self.walk_left = [pygame.transform.flip(i, True, False) for i in walk_images]
#         self.walk_right = walk_images
#         self.hitbox = (self.x + 37, self.y + 11, 29, 95)
#         self.health = 3
#         self.visible = True

#     def draw(self, screen):
#         self.move()
#         if self.visible:
#             if self.walk_count + 1 >= 33:
#                 self.walk_count = 0
#             if self.vel > 0:
#                 screen.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
#                 self.walk_count += 1
#             else:
#                 screen.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
#                 self.walk_count += 1
#             self.hitbox = (self.x + 37, self.y + 11, 29, 95)
#             pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
#             pygame.draw.rect(screen, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((3 - self.health) * 16), 10))
#         pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


#     def move(self):
#         if self.vel > 0:
#             if self.x + self.vel < self.path[-1]:
#                 self.x += self.vel
#             else:
#                 self.vel = self.vel * -1
#                 self.walk_count = 0
#         else:
#             if self.x - self.vel > self.path[0]:
#                 self.x += self.vel
#             else:
#                 self.vel = self.vel * -1
#                 self.walk_count = 0

#     def hit(self):
#         if self.health > 0:
#             self.health -= 1
#         else:
#             self.visible = False
#         return 1