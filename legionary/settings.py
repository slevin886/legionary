
SCREEN_X = 1200
SCREEN_Y = 600
# BACKGROUND = pygame.image.load("./pngs/background.png").convert()
# BACKGROUND = pygame.transform.scale(BACKGROUND, (1200, 600))
FRAMES_PER_SEC = 60
LEVEL_1_PLATFORMS = [
    (0, SCREEN_Y - 40, SCREEN_X * 2, 40), # ground
    (SCREEN_X / 2 - 50, SCREEN_Y * 0.75, 100, 20),
    (SCREEN_X / 2 + 170, SCREEN_Y / 2, 50, 20),
    (SCREEN_X - 170, SCREEN_Y / 3, 50, 20),
    (SCREEN_X + 170, SCREEN_Y / 3, 50, 20)
]

HIGHSCORE_FILE = "highscore.txt"
SPRITESHEET_FILE = "test_sprites/spritesheet_jumper.png"