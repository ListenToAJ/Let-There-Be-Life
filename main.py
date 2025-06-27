import numpy as np
import pygame
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

from life_logic import step, save_life_grid

# CONSTANTS
GRID_SIZE = (100, 100)
PIXEL_SIZE = 20

def setup_display():
    """
    Create window with PyGame and do first display.
    """
    bg_color = (60,60,60)
    screen = pygame.display.set_mode(tuple(x * PIXEL_SIZE for x in GRID_SIZE))
    pygame.display.set_caption("The Game of Life!")
    screen.fill(bg_color)
    pygame.display.flip()
    return screen

def draw_grid(grid: np.array, screen: pygame.display):
    """
    Pass 2d numpy array and draw it to screen (boolean values).
    """
    for y,x in np.ndindex(grid.shape):
        # Get color for pixel value
        pixel_value = grid[y, x]
        color = (255, 255, 255) if pixel_value else (0, 0, 0)

        # Create rect object
        rect = pygame.Rect(x*PIXEL_SIZE+2, y*PIXEL_SIZE+2, PIXEL_SIZE-2, PIXEL_SIZE-2)
        pygame.draw.rect(surface=screen, color=color, rect=rect)        

    pygame.display.flip()

def update_grid(grid: np.array, click_pos: tuple, button: int):
    """
    Take click pos and button click and modify grid.
    """
    # Convert click pos coords to grid space coords
    grid_space = tuple(x // PIXEL_SIZE for x in click_pos)

    # Click conditional
    if button == 1:
        grid[grid_space] = True
    elif button == 3:
        grid[grid_space] = False
    else:
        raise ValueError("How tf did we get here brother?")
    

def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select Life Setup",
        filetypes=[("NumPy Files", "*.npy"), ("All Files", "*.*")]
    )
    if file_path:
        print("Selected file:", file_path)
    return file_path
    

if __name__ == '__main__':
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Setup screen size    
    screen = setup_display()

    # Create and draw grid
    grid = np.zeros(GRID_SIZE, dtype=bool)

    # Main loop
    running = True
    playing = False
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    playing ^= True
                    print(f"Playing bool is set to: {playing}")

                elif event.key == pygame.K_RIGHT:
                    grid = step(grid=grid)

                elif event.key == pygame.K_s:
                    save_life_grid(array=grid)

                elif event.key == pygame.K_o:
                    selected_file = open_file_dialog()
                    grid = np.load(selected_file)

                elif event.key == pygame.K_r:
                    grid.fill(False)
                    
        if playing:
            grid = step(grid=grid)
            time.sleep(0.01)

        draw_grid(grid=grid, screen=screen)
        