import numpy as np

class Food:
    def __init__(self):
        self.x = None
        self.y = None
    def relocate( self, grid ):
        self.x = int(np.random.random() * grid.shape[0])
        self.y = int(np.random.random() * grid.shape[1])
        while grid[self.x][self.y] != 0:
            self.x = int(np.random.random() * grid.shape[0])
            self.y = int(np.random.random() * grid.shape[1])
