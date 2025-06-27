# life_display.py

import pygame
import numpy as np

GRID_COLOR = (60, 60, 60)


def setup_display(grid_size: tuple, pixel_size: int):
    """
    Setup Pygame display for future use.
    """
    screen = pygame.display.set_mode(tuple(x * pixel_size for x in grid_size))
    pygame.display.set_caption("The Game of Life!")
    screen.fill(GRID_COLOR)
    pygame.display.flip()

    return screen


def draw_grid(grid: np.ndarray, pixel_size: int, screen):
    """
    Take game grid and draw it to the screen.
    """
    for y, x in np.ndindex(grid.shape):
        # Get color for pixel value
        color = (255, 255, 255) if grid[y, x] else (0, 0, 0)

        # Draw rect object for cell
        rect = pygame.Rect(
            x * pixel_size + 2, y * pixel_size + 2, pixel_size - 2, pixel_size - 2
        )
        pygame.draw.rect(surface=screen, color=color, rect=rect)

    pygame.display.flip()
