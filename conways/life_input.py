# life_input.py

from tkinter import filedialog
import numpy as np
from datetime import datetime

def update_grid(grid: np.ndarray, pixel_size: int, click_pos: tuple, button_clicked: int):
    """
    Take a mouse input and update grid based on it.
    """
    # Convert clicked coords to grid location
    y = min(max(click_pos[1] // pixel_size, 0), grid.shape[0] - 1)
    x = min(max(click_pos[0] // pixel_size, 0), grid.shape[1] - 1)

    # Draw and erase
    if button_clicked == 1:
        grid[y, x] = True
    elif button_clicked ==3:
        grid[y, x] = False
    else:
        raise ValueError("Unknown mouse button!")

def save_life_grid(grid: np.ndarray, prefix="life"):
    """
    Save current grid setup to timestamped .npy file.
    """
    timestamp = datetime.now().strftime("%H-%M-%S")
    filename = f"./{prefix}_{timestamp}.npy"
    np.save(filename, grid)
    print(f"Saved: {filename}")

def load_in_file(grid: np.ndarray) -> np.ndarray:
    """
    Open and overlay file on existing grid.
    """
    # Open and load grid from dialog
    file_path = filedialog.askopenfilename(
        title="Select Life Setup",
        filetypes=[("NumPy Files", "*.npy"), ("All Files", "*.*")],
    )
    if file_path:
        print("Selected file:", file_path)
    new_grid = np.load(file_path)

    # Determine the overlapping region
    rows = min(grid.shape[0], new_grid.shape[0])
    cols = min(grid.shape[1], new_grid.shape[1])

    # Overwrite only the overlapping region
    grid[:rows, :cols] = new_grid[:rows, :cols]

    return grid