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

def update_grid(grid: np.array, click_pos: tuple, button: int):
    # Convert click pos coords to grid space coords
    grid_space = tuple(x // PIXEL_SIZE for x in click_pos)

    if button == 1:
        grid[grid_space] = True
    elif button == 3:
        grid[grid_space] = False
    else:
        raise ValueError("How tf did we get here brother?")

if __name__ == '__main__':
    # Setup screen size    
    screen = setup_display()

    # Create and draw grid
    grid = np.zeros(GRID_SIZE, dtype=bool)

    # Main loop
    running = True
    dragging_left = False
    dragging_right = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mouse down event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging_left = True
                    update_grid(grid=grid, click_pos=tuple(reversed(event.pos)), button=event.button)
                if event.button == 3:
                    dragging_right = True
                    update_grid(grid=grid, click_pos=tuple(reversed(event.pos)), button=event.button)
            # Mouse up event
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_left = False
                if event.button == 3:
                    dragging_right = False
            # Mouse drag event
            elif event.type == pygame.MOUSEMOTION:
                if dragging_left:
                    update_grid(grid=grid, click_pos=tuple(reversed(event.pos)), button=1)
                if dragging_right:
                    update_grid(grid=grid, click_pos=tuple(reversed(event.pos)), button=3)

            draw_grid(grid=grid, screen=screen)


        