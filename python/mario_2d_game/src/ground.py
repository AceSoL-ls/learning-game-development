import pygame
from settings import WIDTH, HEIGHT, GROUND_SPEED

class GroundTile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed_scale=1):
        # Move tile left
        self.rect.x -= int(GROUND_SPEED * speed_scale)
        # Kill if off-screen
        if self.rect.right < 0:
            self.kill()


class Ground:
    def __init__(self):
        # Load ground image
        self.image = pygame.image.load("assets/environment/ground.png").convert_alpha()
        self.height = self.image.get_height()
        self.tiles = pygame.sprite.Group()

        # Fill screen with enough tiles
        for i in range(WIDTH // self.image.get_width() + 2):
            tile = GroundTile(i * self.image.get_width(), HEIGHT - self.height, self.image)
            self.tiles.add(tile)

    def update(self, speed_scale=1):
        self.tiles.update(speed_scale)

        # Add new tile if last one is moving into screen
        if self.tiles:
            last_tile = max(self.tiles, key=lambda t: t.rect.x)
            if last_tile.rect.right < WIDTH:
                new_tile = GroundTile(last_tile.rect.right, HEIGHT - self.height, self.image)
                self.tiles.add(new_tile)

    def draw(self, screen):
        self.tiles.draw(screen)