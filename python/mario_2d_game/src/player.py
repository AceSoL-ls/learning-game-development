# Player class handles Mario image loading, animations, jumping, gravity, and ground collision

import pygame
from settings import GRAVITY, JUMP_FORCE, HEIGHT

# Desired Mario size (adjust as needed)
MARIO_WIDTH = 60
MARIO_HEIGHT = 70

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # --- Load and scale images ---
        self.image_run = [
            pygame.transform.scale(
                pygame.image.load("assets/mario/run1.png").convert_alpha(),
                (MARIO_WIDTH, MARIO_HEIGHT)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/mario/run2.png").convert_alpha(),
                (MARIO_WIDTH, MARIO_HEIGHT)
            )
        ]
        self.image_jump = pygame.transform.scale(
            pygame.image.load("assets/mario/jump.png").convert_alpha(),
            (MARIO_WIDTH, MARIO_HEIGHT)
        )
        self.image_idle = pygame.transform.scale(
            pygame.image.load("assets/mario/idle.png").convert_alpha(),
            (MARIO_WIDTH, MARIO_HEIGHT)
        )

        # --- Animation ---
        self.frame_index = 0
        self.image = self.image_idle

        # --- Position and physics ---
        self.rect = self.image.get_rect(midbottom=(100, 260))
        self.velocity_y = 0
        self.on_ground = True

    def jump(self):
        """Make Mario jump only if he is on the ground."""
        if self.on_ground:
            self.velocity_y = JUMP_FORCE   # JUMP_FORCE must be negative
            self.on_ground = False

    def apply_gravity(self, ground_group):
        """Apply gravity and check collision with ground tiles."""
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check collision with ground tiles
        collided_ground = pygame.sprite.spritecollide(self, ground_group, False)
        if collided_ground and self.velocity_y >= 0:
            ground_tile = collided_ground[0]
            self.rect.bottom = ground_tile.rect.top
            self.on_ground = True
            self.velocity_y = 0
        else:
            self.on_ground = False

        # If Mario falls off screen → game over trigger
        if self.rect.top > HEIGHT:
            self.kill()  # remove Mario sprite (main.py should detect this and set game_active = False)

    def animate(self):
        """Switch Mario’s sprite depending on state."""
        if not self.on_ground:
            self.image = self.image_jump
        else:
            # Run cycle when on ground
            self.frame_index += 0.15
            if self.frame_index >= len(self.image_run):
                self.frame_index = 0
            self.image = self.image_run[int(self.frame_index)]

    def update(self, ground_group):
        """Update Mario each frame."""
        self.apply_gravity(ground_group)
        self.animate()