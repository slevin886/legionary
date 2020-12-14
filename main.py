import pygame
from os import path
from legionary.player import Player, LoadSprites
from legionary.enemies import Enemy
from legionary.projectiles import Projectile
from legionary.platforms import Platform
from legionary.settings import *



# pygame.init()


# CLOCK = pygame.time.Clock()
# SCREEN_X = 1200
# SCREEN_Y = 600
# SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
# BACKGROUND = pygame.image.load("./pngs/background.png").convert()
# BACKGROUND = pygame.transform.scale(BACKGROUND, (1200, 600))
# FRAMES_PER_SEC = 27


class Legionary:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
        pygame.display.set_caption("Legionary")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.match_font("comicsans")
        self.running = True
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HIGHSCORE_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        img_dir = path.join(self.dir, SPRITESHEET_FILE)
        self.sprite_sheet = LoadSprites(img_dir)

    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in LEVEL_1_PLATFORMS:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FRAMES_PER_SEC)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False) # False, don't delete on colission
        # check if player lands on platform
        if self.player.vel.y > 0:
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
                self.player.jumping = False
        # Scroll screen
        if self.player.pos.x > SCREEN_X / 2 and self.player.vel.x > 1:
            print(self.player.pos.x, SCREEN_X / 2)
            self.player.pos.x = SCREEN_X / 2 - 2  # -2 prevents friction from hanging over mid  
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.right < 0:
                    plat.kill()
        # falling death
        if self.player.rect.bottom > SCREEN_Y:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(10, self.player.vel.y)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.jump()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(25, 25, f"Score: {self.score}", 22, (255, 0, 0))
        pygame.display.flip()

    def draw_text(self, x, y, text, size, color):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FRAMES_PER_SEC / 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    

    def show_start_screen(self):
        self.screen.fill((160, 200, 29))
        self.draw_text(SCREEN_X / 2, SCREEN_Y / 2, "Legionary", 80, (0, 0, 0))
        self.draw_text(SCREEN_X / 2, SCREEN_Y / 2 + 100, "Press Enter to Begin", 80, (0, 0, 0))
        self.draw_text(SCREEN_X / 2, SCREEN_Y / 2 + 150, f"High Score: {self.highscore}", 80, (0, 0, 0))
        pygame.display.flip()
        self.wait_for_key()



    def show_game_over_screen(self):
        # make sure they're not just quitting
        if not self.running:
            return
        self.screen.fill((250, 0, 0))
        self.draw_text(SCREEN_X / 2, SCREEN_Y / 2, "GAME OVER", 80, (0, 0, 0))
        self.draw_text(SCREEN_X / 2, SCREEN_Y / 2 + 100, f"Final Score: {self.score}", 60, (0, 0, 0))
        self.draw_text(SCREEN_X / 2, SCREEN_Y / 2 + 150, "Press Enter to Play Again", 60, (0, 0, 0))
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(SCREEN_X / 2, SCREEN_Y / 2 + 175, f"Congrats! New highscore!", 60, (0, 0, 0))
            with open(path.join(self.dir, HIGHSCORE_FILE), 'w') as f:
                f.write(str(self.score))
        pygame.display.flip()
        self.wait_for_key()

legionary = Legionary()
legionary.show_start_screen()

while legionary.running:
    legionary.new()
    legionary.show_game_over_screen()

pygame.quit()
# font = pygame.font.SysFont("comicsans", 14, bold=True)

# def load_images(
#     loc="player", 
#     image_suffix="r", 
#     transform=False, 
#     num_images=10, 
#     size_x=128, 
#     size_y=128, 
#     remove_white=True
#     ):
#     images = []
#     for i in range(1, num_images):
#         filepath =  f"pngs/{loc}/{image_suffix}{i}.png"
#         img = pygame.image.load(filepath)
#         if remove_white:
#             img.set_colorkey((255, 255, 255))
#             img = img.convert_alpha()
#         if transform:
#             images.append(pygame.transform.scale(img, (size_x, size_y)))
#         else:
#             images.append(img)
#     return images

# player_walk = load_images(transform=True)
# enemy_walk = load_images(
#     loc="barbarian", 
#     image_suffix="r", 
#     num_images=12, 
#     remove_white=False,
#     transform=True,
#     # size_x=150,
#     # size_y=150 
    
#     )

# bullets = []
# reload_timer = 0
# score = 0
# player = Player(50, 450, 128, 128, walk_images=player_walk, vel=8)
# enemy = Enemy(100, 440, 64, 64, 250, walk_images=enemy_walk)
# all_platforms = pygame.sprite.Group()
# all_platforms.add(Platform(125, 400, 100, 10))

# def redraw_screen(screen, player, bullets, enemy, score, font, all_platforms):
#     screen.blit(BACKGROUND, (0,0))
#     score_bar = font.render(f"Score: {score}", 1, (0, 0, 0))
#     screen.blit(score_bar, (SCREEN_X - 100, 20))
#     player.draw(screen)
#     enemy.draw(screen)
#     all_platforms.draw(screen)
#     for bullet in bullets:
#         bullet.draw(screen)
#     pygame.display.update()




# running = True
# while running:
#     CLOCK.tick(27)
#     if reload_timer > 0:
#         if reload_timer > 3:
#             reload_timer = 0
#         else:
#             reload_timer += 1
#     # pygame.time.delay(50)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     if (player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and 
#         player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]):
#         if (player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and 
#             player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]):
#             score -= player.hit()
#     for ind, bullet in enumerate(bullets):
#         if (bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and 
#             bullet.y + bullet.radius > enemy.hitbox[1]):
#             if (bullet.x + bullet.radius > enemy.hitbox[0] and 
#                 bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]):
#                 score += enemy.hit()
#                 bullets.pop(ind)
#         if 0 < bullet.x and bullet.x < SCREEN_X:
#             bullet.x += bullet.vel
#         else:
#             bullets.pop(ind)

#     landing = pygame.sprite.spritecollide(player, all_platforms, False)
#     if landing and player.rect.y - player.rect.height <= landing[0].rect.y:
#         player.jump = False
#         player.y = landing[0].rect.y + 1
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_SPACE] and reload_timer == 0:
#         reload_timer = 1
#         if player.left:
#             bullet_right = -1
#         else: 
#             bullet_right = 1
#         if len(bullets) < 5:
#             bullets.append(
#                 Projectile(
#                     round(player.x + player.width // 2), 
#                     round(player.y + player.height // 2),
#                     6,
#                     bullet_right, 
#                     (0, 0, 0)
#                     )
#                 )
#     if keys[pygame.K_LEFT] and player.x > player.vel:
#         player.x -= player.vel
#         player.left = True
#         player.right = False
#         player.standing = False
#     elif keys[pygame.K_RIGHT] and player.x < (SCREEN_X - player.width - player.vel):
#         player.x += player.vel
#         player.left = False
#         player.right = True
#         player.standing = False
#     else:
#         player.standing = True
#         player.walk_count = 0
#     if not player.jump:
#         if keys[pygame.K_UP]:
#             player.jump = True
#             player.standing = True
#             player.walk_count = 0
#     else:
#         player.standing = True
#         if player.jump_count >= -10:
#             player.y -= (abs(player.jump_count) * player.jump_count) * 0.5
#             player.jump_count -= 1
#         else:
#             player.jump = False
#             player.jump_count = 10
#     redraw_screen(SCREEN, player, bullets, enemy, score, font, all_platforms)
# pygame.quit()
