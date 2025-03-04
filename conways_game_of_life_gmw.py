# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#grid size
N = 70

# innitialize the grid with random binary values (0s and 1s)
grid = np.random.choice([0, 1], size=(N, N), p=[0.7, 0.3])

# creae my color map where 0 (dead cells) are black and 1 (alive cells) are assigned a random color
color_map = np.random.rand(N, N, 3)  # random RGB values for each cell color assignment

def update(frame):
    """
    purpose: to update the Game of Life grid for the next frame.

    - applies Conway’s Game of Life rules to determine cell survival.
    - updates the grid state based on the number of live neighbors.
    - then assigns new colors to newly born cells.

    params:
    frame (int): current frame number (unused, but required for animation set up).

    returns:
    img (matplotlib.image.AxesImage,): updated image for animation returning each frame.
    """
    global grid, color_map  # global variables to modify the grid and color map
    new_grid = grid.copy()  #  a copy to store the next generation without modifying the original grid or frames

    for i in range(N):
        for j in range(N):
            # first, to count the number of live neighbors (using a toroidal (wrapped) grid)
            neighbors = sum([
                grid[(i + x) % N, (j + y) % N]  # then wrap around the edges to simulate an infinite grid
                for x in [-1, 0, 1] for y in [-1, 0, 1]
                if (x, y) != (0, 0)  # but exclude the cell itself
            ])

            # ---- Conway's Game of Life rules ------------------------------------
            if grid[i, j] == 1:  # 1) if the cell is currently alive,
                if neighbors < 2 or neighbors > 3: # if neighbors are < 2 or > 3,
                    new_grid[i, j] = 0  # then the cell will die from underpopulation / overpopulation.
            else:  # if the cell is currently dead ...
                if neighbors == 3: #but has exactly three neighbors ...
                    new_grid[i, j] = 1  # then it comes back to life! (reproduction)
                    color_map[i, j] = np.random.rand(3)  # the newborn cell gets a new random color

    grid = new_grid  # update the grid with each new state

    # to update the visualization: alive or newborn cells take their current assigned color, dead cells remain black
    img.set_array(np.where(grid[:, :, None] == 1, color_map, [0, 0, 0]))

    return img,  # return the updated image frame for the animation:

# figure and axis
fig, ax = plt.subplots()

img = ax.imshow(np.where(grid[:, :, None] == 1, color_map, [0, 0, 0]), interpolation="nearest")
ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

# animation
ani = animation.FuncAnimation(fig, update, frames=450, interval=100, blit=False)

# show:
from IPython.display import HTML
display(HTML(ani.to_jshtml()))

