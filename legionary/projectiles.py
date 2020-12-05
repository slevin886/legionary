import pygame

class Projectile:

    def __init__(self, x, y, radius, direction, color, vel=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = direction
        self.color = color
        self.vel = vel * direction
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)