import pygame
from legionary.player import Player
from legionary.enemies import Enemy
from legionary.projectiles import Projectile


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

def load_images(
    loc="player", 
    image_suffix="r", 
    transform=False, 
    num_images=10, 
    size_x=128, 
    size_y=128, 
    remove_white=True
    ):
    images = []
    for i in range(1, num_images):
        filepath =  f"pngs/{loc}/{image_suffix}{i}.png"
        img = pygame.image.load(filepath)
        if remove_white:
            img.set_colorkey((255, 255, 255))
            img = img.convert_alpha()
        if transform:
            images.append(pygame.transform.scale(img, (size_x, size_y)))
        else:
            images.append(img)
    return images

player_walk = load_images(transform=True)
enemy_walk = load_images(loc="enemy1", image_suffix="r", num_images=12, remove_white=False)

bullets = []
reload_timer = 0
score = 0
player = Player(50, 440, 128, 128, walk_images=player_walk, vel=8)
enemy = Enemy(100, 440, 64, 64, 250, walk_images=enemy_walk)

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
