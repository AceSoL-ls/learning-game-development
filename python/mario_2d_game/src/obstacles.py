# This is a generator module for obstacles in the game application
# It handles obstacle image loading, positioning, movement and removal when off-screen

import pygame, random
from settings import GROUND_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()   # Initialize parent Sprite class
        
        # --- Randomly choose an obstacle type ---
        obstacle_types = ["flower", "pipe"]          # List of available obstacle types
        chosen_type = random.choice(obstacle_types)  # Pick one at random each time
        
        # --- Load image and set position depending on type ---
        if chosen_type == "flower":
            original_image = pygame.image.load("assets/obstacles/flower.png").convert_alpha()
            # Scale to 50x50 pixels (adjust as needed)
            self.image = pygame.transform.scale(original_image, (60, 60))
            # Spawn at a random x position between 400 and 600
            self.rect = self.image.get_rect(midbottom=(random.randint(400, 600), 260))
        
        elif chosen_type == "pipe":
            original_image = pygame.image.load("assets/obstacles/pipe.png").convert_alpha()
            # Scale to 80x120 pixels (pipes usually taller, adjust as needed)
            self.image = pygame.transform.scale(original_image, (70, 80))
            # Spawn at a random x position between 500 and 700
            self.rect = self.image.get_rect(midbottom=(random.randint(500, 700), 260))
            
    def update(self):
        # --- Move obstacle left across the screen ---
        self.rect.x -= GROUND_SPEED
        
        # --- Remove obstacle when it goes off-screen ---
        if self.rect.right < 0:
            self.kill()