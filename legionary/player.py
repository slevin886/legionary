import pygame


class Player:

    def __init__(self, x, y, width, height, walk_images, vel=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.left = False
        self.right = False
        self.jump = False
        self.jump_count = 10
        self.walk_count = 0
        self.walk_right = walk_images
        self.walk_left = [pygame.transform.flip(i, True, False) for i in walk_images]
        # self.standing_image = walk_right[0]
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 54)
        self.health = 10

    def draw(self, screen):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                screen.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                screen.blit(self.walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.left:
                screen.blit(self.walk_left[0], (self.x, self.y))
            else:
                screen.blit(self.walk_right[0], (self.x, self.y))
        if self.left: # correct for image turninig left:
            self.hitbox = (self.x + 55, self.y + 3, 35, 95)
        else:
            self.hitbox = (self.x + 25, self.y + 3, 35, 95)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        self.health -= 1
        return 1