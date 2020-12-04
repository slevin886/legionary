import pygame
from legionary.player import Player

class Enemy:
    def __init__(self, x, y, width, height, end, vel=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.end = end
        self.walk_count = 0
        self.path = [self.x, self.end]
        self.walk_left = [pygame.image.load(f'pngs/L{i}E.png') for i in range(1, 12)]
        self.walk_right = [pygame.image.load(f'pngs/R{i}E.png') for i in range(1, 12)]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
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
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((3 - self.health) * 16), 10))
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


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


def redraw_screen(screen, player, bullets, enemy, score, font):
    screen.blit(BACKGROUND, (0,0))
    score_bar = font.render(f"Score: {score}", 1, (0, 0, 0))
    screen.blit(score_bar, (SCREEN_X - 100, 20))
    player.draw(screen)
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()

pygame.init()
pygame.display.set_caption("Legionary")

CLOCK = pygame.time.Clock()
SCREEN_X = 1200
SCREEN_Y = 600
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
BACKGROUND = pygame.image.load("./pngs/background.png").convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (1200, 600))

font = pygame.font.SysFont("comicsans", 14, bold=True)
# walk_left = [pygame.image.load(f'pngs/player/L{i}.png') for i in range(1, 10)]
walk_right = []
for i in range(1, 10):
    filepath =  f"pngs/player/r{i}.png"
    img = pygame.image.load(str(filepath))
    img.set_colorkey((255, 255, 255))
    walk_right.append(pygame.transform.scale(img.convert_alpha(), (128, 128)))

bullets = []
reload_timer = 0
score = 0
player = Player(50, 440, 128, 128, walk_images=walk_right, vel=8)
enemy = Enemy(100, 440, 64, 64, 250)

running = True
while running:
    CLOCK.tick(27)
    if reload_timer > 0:
        if reload_timer > 3:
            reload_timer = 0
        else:
            reload_timer += 1
    # pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if (player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and 
        player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]):
        if (player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and 
            player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]):
            score -= player.hit()
    for ind, bullet in enumerate(bullets):
        if (bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and 
            bullet.y + bullet.radius > enemy.hitbox[1]):
            if (bullet.x + bullet.radius > enemy.hitbox[0] and 
                bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]):
                score += enemy.hit()
                bullets.pop(ind)
        if 0 < bullet.x and bullet.x < SCREEN_X:
            bullet.x += bullet.vel
        else:
            bullets.pop(ind)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and reload_timer == 0:
        reload_timer = 1
        if player.left:
            bullet_right = -1
        else: 
            bullet_right = 1
        if len(bullets) < 5:
            bullets.append(
                Projectile(
                    round(player.x + player.width // 2), 
                    round(player.y + player.height // 2),
                    6,
                    bullet_right, 
                    (0, 0, 0)
                    )
                )
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False
    elif keys[pygame.K_RIGHT] and player.x < (SCREEN_X - player.width - player.vel):
        player.x += player.vel
        player.left = False
        player.right = True
        player.standing = False
    else:
        player.standing = True
        player.walk_count = 0
    if not player.jump:
        if keys[pygame.K_UP]:
            player.jump = True
            player.standing = True
            player.walk_count = 0
    else:
        player.standing = True
        if player.jump_count >= -10:
            player.y -= (abs(player.jump_count) * player.jump_count) * 0.5
            player.jump_count -= 1
        else:
            player.jump = False
            player.jump_count = 10
    redraw_screen(SCREEN, player, bullets, enemy, score, font)
pygame.quit()
