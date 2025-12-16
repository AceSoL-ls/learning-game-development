# This section is for utilities used across the game application
import pygame

def draw_text(screen, text, size, pos, color=(0, 0, 0)):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)