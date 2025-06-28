# life_display.py

import pygame
import numpy as np
from scipy.ndimage import gaussian_filter

GRID_COLOR = (40, 40, 40)

def setup_display(grid_size: tuple, pixel_size: int):
    """
    Setup Pygame display for future use.
    """
    screen = pygame.display.set_mode(tuple((x * pixel_size) + 2 for x in reversed(grid_size)))
    pygame.display.set_caption("The Game of Life!")
    screen.fill(GRID_COLOR)
    pygame.display.flip()

    return screen

def create_glow_surface(radius, color=(180, 180, 255), max_alpha=60):
    size = radius * 2
    glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    arr = pygame.surfarray.pixels_alpha(glow_surf)

    # Create radial gradient for alpha channel: max at center, fading to 0 at edges
    for y in range(size):
        for x in range(size):
            dx = x - radius
            dy = y - radius
            dist = np.sqrt(dx * dx + dy * dy)
            alpha = max(0, max_alpha * (1 - dist / radius))
            arr[x, y] = int(alpha)

    del arr  # unlock the surface

    # Fill RGB with the glow color, keep alpha separate
    rgb_arr = pygame.surfarray.pixels3d(glow_surf)
    rgb_arr[:, :, 0] = color[0]
    rgb_arr[:, :, 1] = color[1]
    rgb_arr[:, :, 2] = color[2]
    del rgb_arr

    return glow_surf

def draw_grid(grid: np.ndarray, pixel_size: int, screen, glow_surf):
    # Fill border color
    screen.fill(GRID_COLOR)

    radius = glow_surf.get_width() // 2

    # Draw all black tiles
    for y, x in np.ndindex(grid.shape):
        if grid[y, x] == False:
            rect = pygame.Rect(
                x * pixel_size + 2, y * pixel_size + 2, pixel_size - 2, pixel_size - 2
            )
            pygame.draw.rect(screen, (0, 0, 0), rect)

    # Draw glow and then white tiles
    for y, x in np.ndindex(grid.shape):
        if grid[y, x]:
            pos = (
                x * pixel_size + pixel_size // 2 - radius,
                y * pixel_size + pixel_size // 2 - radius,
            )
            screen.blit(glow_surf, pos)

            rect = pygame.Rect(
                x * pixel_size + 0, y * pixel_size + 0, pixel_size + 1, pixel_size + 1
            )
            pygame.draw.rect(screen, (255, 255, 255), rect)
