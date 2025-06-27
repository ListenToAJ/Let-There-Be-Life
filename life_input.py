# life_input.py

from tkinter import filedialog
import numpy as np

def update_grid(grid: np.ndarray, pixel_size: int, click_pos: tuple, button_clicked: int):
    """
    Take a mouse input and update grid based on it.
    """
    # Convert clicked coords to grid location
    y, x = (coord // pixel_size for coord in reversed(click_pos))

    # Draw and erase
    if button_clicked == 1:
        grid[y, x] = True
    elif button_clicked ==3:
        grid[y, x] = False
    else:
        raise ValueError("Unknown mouse button!")

def open_file_dialog():
    """
    Use TKinter file dialog to cleanly open .npy files.
    """
    file_path = filedialog.askopenfilename(
        title="Select Life Setup",
        filetypes=[("NumPy Files", "*.npy"), ("All Files", "*.*")],
    )
    if file_path:
        print("Selected file:", file_path)
    return file_path
