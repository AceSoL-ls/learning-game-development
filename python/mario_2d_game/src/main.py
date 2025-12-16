import pygame, sys, random
from settings import WIDTH, HEIGHT, FPS, OBSTACLE_SPAWN_TIME
from player import Player
from ground import Ground
from obstacles import Obstacle
from utilities import draw_text

pygame.init()
pygame.mixer.init()   # initialize sound system

# Load soundtrack
game_music = pygame.mixer.Sound("assets/soundtrack/OG_soundtrack.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Runner")
clock = pygame.time.Clock()

background = pygame.image.load("assets/environment/background.png").convert()

# Sprite groups
player = pygame.sprite.GroupSingle(Player())
obstacles = pygame.sprite.Group()

# Ground instance (manages tiles)
ground = Ground()

# Game states
game_start = False   # waiting for any key to start
game_active = False  # running gameplay
score = 0
high_score = 0

# Obstacle timer
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, OBSTACLE_SPAWN_TIME)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Press any key to start
        if not game_start and event.type == pygame.KEYDOWN:
            game_start = True
            game_active = True
            score = 0
            obstacles.empty()
            player = pygame.sprite.GroupSingle(Player())

        # Spawn obstacles only during active game
        if event.type == SPAWN_EVENT and game_active:
            obstacles.add(Obstacle())

        # Jump only during active game
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                player.sprite.jump()

        # Restart after game over
        if event.type == pygame.KEYDOWN and game_start and not game_active:
            if event.key == pygame.K_SPACE:
                game_active = True
                score = 0
                obstacles.empty()
                player = pygame.sprite.GroupSingle(Player())

    # ------------- Start Screen -------------
    if not game_start:
        screen.blit(background, (0, 0))
        ground.update(1)   # slow scroll
        ground.draw(screen)

        # Show Mario idle sprite
        player.sprite.image = player.sprite.image_idle
        player.draw(screen)

        draw_text(screen, "Mario Runner", 80, (WIDTH // 2, HEIGHT // 4))
        draw_text(screen, "Press ANY key to Start", 40, (WIDTH // 2, HEIGHT // 2))

        game_music.stop()

    # ------------- Game Active -------------
    elif game_active:
        if not pygame.mixer.get_busy():
            game_music.play(-1)   # loop forever

        screen.blit(background, (0, 0))

        # Score
        score += 0.2
        draw_text(screen, f"Score: {int(score)}", 40, (700, 20))

        # Difficulty scaling
        speed_scale = 1 + (score // 100) * 0.1

        # Ground
        ground.update(speed_scale)
        ground.draw(screen)

        # Player (pass ground tiles for collision)
        player.update(ground.tiles)
        player.draw(screen)

        # Obstacles
        obstacles.update()
        obstacles.draw(screen)

        # Collision with obstacles
        if pygame.sprite.spritecollide(player.sprite, obstacles, False):
            game_active = False
            high_score = max(high_score, int(score))
            game_music.stop()

        # Check if Mario fell off screen (sprite killed)
        if not player.sprite.alive():
            game_active = False
            high_score = max(high_score, int(score))
            game_music.stop()

    # ------------- Game Over -------------
    else:
        screen.blit(background, (0, 0))
        ground.update(1)
        ground.draw(screen)

        # Show Mario idle sprite
        if player.sprite:  # recreate idle if sprite killed
            player.sprite.image = player.sprite.image_idle
            player.draw(screen)

        draw_text(screen, "Game Over", 80, (WIDTH // 2, HEIGHT // 4))
        draw_text(screen, f"Score: {int(score)}", 50, (WIDTH // 2, HEIGHT // 2 - 40))
        draw_text(screen, f"High Score: {int(high_score)}", 50, (WIDTH // 2, HEIGHT // 2 + 20))
        draw_text(screen, "Press SPACE to Restart", 40, (WIDTH // 2, HEIGHT // 2 + 100))

        game_music.stop()

    pygame.display.update()
    clock.tick(FPS)