import numpy as np

class Food:
    def __init__(self):
        self.x = 2 * 1
        self.y = 2 * 1

    def relocate( self, grid ):
        while grid[self.x][self.y] != 0:
            self.x = int(np.random.random() * grid.shape[0])
            self.y = int(np.random.random() * grid.shape[1])
