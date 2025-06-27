# life_logic.py

import numpy as np

def step(grid: np.ndarray) -> np.ndarray:
    """
    Apply Conway's Game of Life rules and return next generation grid.
    """
    next_step = grid.copy()
    cell_neighbors = [
        (-1, -1), (-1, 0), (-1, +1),
        (0, -1),           (0, +1),
        (+1, -1), (+1, 0), (+1, +1),
    ]

    for y, x in np.ndindex(grid.shape):
        # Get neighbor count
        neighbors = sum(
            grid[(y + dy) % grid.shape[0], (x + dx) % grid.shape[1]]
            for dy, dx in cell_neighbors
        )

        if grid[y, x]:
            next_step[y, x] = (neighbors in (2, 3))   # Only way for cell to survive
        else:
            next_step[y, x] = (neighbors == 3)  # Only way for new cells to emerge

    return next_step
