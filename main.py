import numpy as np
import pygame

# CONSTANTS
GRID_SIZE = (50, 50)
PIXEL_SIZE = 20

def setup_display():
    """
    Create window with PyGame and do first display.
    """
    bg_color = (0,0,0)
    screen = pygame.display.set_mode(tuple(x * PIXEL_SIZE for x in GRID_SIZE))
    pygame.display.set_caption("Hello there!")
    screen.fill(bg_color)
    pygame.display.flip()
    return screen

def draw_grid(grid: np.array, screen: pygame.display):
    """
    Pass 2d numpy array and draw it to screen (boolean values)
    """
    for y,x in np.ndindex(grid.shape):
        # Get color for pixel value
        pixel_value = grid[y, x]
        color = (255, 255, 255) if pixel_value else (0, 0, 0)

        # Create rect object
        rect = pygame.Rect(x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
        pygame.draw.rect(surface=screen, color=color, rect=rect)        

    pygame.display.flip()

if __name__ == '__main__':
    # Setup screen size    
    screen = setup_display()

    # Create and draw grid
    grid = np.zeros(GRID_SIZE, dtype=bool)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = tuple(reversed(event.pos))
                print(f"Mouse clicked at: {click_pos}")
                grid_space = tuple(x // PIXEL_SIZE for x in click_pos)
                print(f"Grid space clicked is: {grid_space}")
                grid[grid_space] = True
                draw_grid(grid=grid, screen=screen)
        