import pygame


class Enemy:
    def __init__(self, x, y, width, height, end, walk_images, vel=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.end = end
        self.walk_count = 0
        self.path = [self.x, self.end]
        self.walk_left = [pygame.transform.flip(i, True, False) for i in walk_images]
        self.walk_right = walk_images
        self.hitbox = (self.x + 37, self.y + 11, 29, 95)
        self.health = 3
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0
            if self.vel > 0:
                screen.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                screen.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            self.hitbox = (self.x + 37, self.y + 11, 29, 95)
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((3 - self.health) * 16), 10))
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[-1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        return 1