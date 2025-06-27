import numpy as np
import pygame

def setup_display(screen_size: tuple, pixel_size: int):
    """
    Create window with PyGame and do first display.
    """
    bg_color = (0,0,0)
    screen = pygame.display.set_mode(tuple(x * pixel_size for x in screen_size))
    pygame.display.set_caption("Hello there!")
    screen.fill(bg_color)
    pygame.display.flip()
    return screen

def draw_grid(grid: np.array, pixel_size: int, screen: pygame.display, inner_border: int):
    for y,x in np.ndindex(grid.shape):
        # Get color for pixel value
        pixel_value = grid[y, x]
        color = (255, 255, 255) if pixel_value else (0, 0, 0)

        # Create rect object
        rect = pygame.Rect(x*pixel_size, y*pixel_size, pixel_size, pixel_size)
        pygame.draw.rect(surface=screen, color=color, rect=rect)        
    
    pygame.display.flip()

if __name__ == '__main__':
    # Setup screen size
    grid_size = (50, 50)
    pixel_size = 20
    screen = setup_display(screen_size=grid_size, pixel_size=pixel_size)

    # Create and draw grid
    grid = np.zeros(grid_size, dtype=bool)
    grid[0][0] = True
    grid[0][49] = True
    grid[49][0] = True
    grid[49][49] = True

    draw_grid(grid=grid, pixel_size=pixel_size, screen=screen, inner_border=1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        