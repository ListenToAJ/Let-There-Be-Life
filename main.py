# main.py

import numpy as np
import pygame
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

from life_logic import step, save_life_grid
from life_input import update_grid, open_file_dialog
from life_display import setup_display, draw_grid

# CONSTANTS
GRID_SIZE = (100, 100)
PIXEL_SIZE = 20

if __name__ == '__main__':
    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()

    # Setup screen size
    screen = setup_display(grid_size=GRID_SIZE, pixel_size=PIXEL_SIZE)

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
                    update_grid(grid=grid, pixel_size=PIXEL_SIZE, click_pos=event.pos, button_clicked=event.button)
                if event.button == 3:
                    dragging_right = True
                    update_grid(
                        grid=grid,
                        pixel_size=PIXEL_SIZE,
                        lick_pos=event.pos,
                        button_clicked=event.button,
                    )

            # Mouse up event
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_left = False
                if event.button == 3:
                    dragging_right = False

            # Mouse drag event
            elif event.type == pygame.MOUSEMOTION:
                if dragging_left:
                    update_grid(
                        grid=grid,
                        pixel_size=PIXEL_SIZE,
                        click_pos=event.pos,
                        button_clicked=1,
                    )
                if dragging_right:
                    update_grid(
                        grid=grid,
                        pixel_size=PIXEL_SIZE,
                        click_pos=event.pos,
                        button_clicked=3,
                    )

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

        draw_grid(grid=grid, pixel_size=PIXEL_SIZE, screen=screen)
