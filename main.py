# main.py

import numpy as np
import pygame
import shutil
import time
import sys
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

from conways.life_logic import *
from conways.life_input_output import *
from conways.life_display import *

# CONSTANTS
GRID_SIZE = (30, 30)
PIXEL_SIZE = 35

def run_game():
        # Hide the main tkinter window (Only used for file dialog)
    root = tk.Tk()
    root.withdraw()

    # Setup screen size
    screen = setup_display(grid_size=GRID_SIZE, pixel_size=PIXEL_SIZE)
    
    # Bloom settings
    glow_radius = int(PIXEL_SIZE * 2.5)
    glow_surf = create_glow_surface(glow_radius, max_alpha=40)

    # Main loop
    grid = np.zeros(GRID_SIZE, dtype=bool)
    running = True
    playing = False
    recording = False
    frame_num = 0
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
                    update_grid(
                        grid=grid,
                        pixel_size=PIXEL_SIZE,
                        click_pos=event.pos,
                        button_clicked=event.button,
                    )
                if event.button == 3:
                    dragging_right = True
                    update_grid(
                        grid=grid,
                        pixel_size=PIXEL_SIZE,
                        click_pos=event.pos,
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
                # Play / Pause with 'p' key
                if event.key == pygame.K_p:
                    if recording:
                        # Stop recording on any 'p' or 'shift+p'
                        recording = False
                        playing = False
                        frame_num = 0
                        print("Stopping recording\nPaused!")

                        stitch_recording(format="gif")

                    else:
                        # Check if shift is held down
                        if event.mod & pygame.KMOD_SHIFT:
                            # Start recording
                            recording = True
                            print("Starting recording!")

                            temp_dir = "./recordings/.temp"

                            # Remove the whole folder if it exists
                            if os.path.exists(temp_dir):
                                shutil.rmtree(temp_dir)

                            # Recreate the folder
                            os.makedirs(temp_dir)

                        # Toggle playback
                        playing ^= True
                        print("Playing!" if playing else "Paused!")

                        # After recording is stopped, stitch recording

                # Do single step with '→' key
                elif event.key == pygame.K_RIGHT:
                    grid = step(grid=grid)

                # Save current setup with 's' key
                elif event.key == pygame.K_s:
                    if not os.path.exists("./saved"):
                        os.makedirs("./saved")
                    save_life_grid(grid=grid)

                # Open saved file with 'o' key
                elif event.key == pygame.K_o:
                    playing = False
                    grid = load_in_file(grid=grid)

                # Reset the board with 'r' key
                elif event.key == pygame.K_r:
                    grid.fill(False)

        if playing:
            grid = step(grid=grid)
            time.sleep(0.04)

        if recording:
            pygame.image.save(screen, f"./recordings/.temp/{frame_num:05}.png")
            frame_num += 1
        
        draw_grid(grid=grid, pixel_size=PIXEL_SIZE, screen=screen, glow_surf=glow_surf)

        pygame.display.flip()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            np.load(file_path)
            run_game()
        except Exception as e:
            print(f"An error occured: {e}")
    else:
        run_game()
