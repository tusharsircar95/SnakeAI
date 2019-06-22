class Snake:
    def __init__(self,grid):
        origin = int(grid.shape[0]/2)
        self.direction = 'R'
        self.blobs = []
        for i in range(4):
            self.blobs.append((origin-i,origin))
        self.trail = None
        self.remaining_moves = 200
        self.total_moves = 0
    def updateGrid(self, grid):
        for blob in self.blobs:
            grid[blob[0],blob[1]] = 1
        return grid

    def followUp( self ):
        self.trail = self.blobs[-1]
        for i in range(len(self.blobs)-1,0,-1):
            self.blobs[i] = self.blobs[i-1]

    def grow( self ):
        self.blobs.append(self.trail)
        self.remaining_moves = self.remaining_moves + 100

    def didCollide( self, headBlob, grid ):
        if headBlob[0] < 0 or headBlob[0] >= grid.shape[0]:
            #print('Side wall collission')
            return True
        if headBlob[1] < 0 or headBlob[1] >= grid.shape[1]:
            #print ( 'TopBottom wall collission' )
            return True
        #if grid[ headBlob[ 0 ] ][ headBlob[ 1 ] ] == 1:
            #print ( 'Self collission' )
        return grid[ headBlob[ 0 ] ][ headBlob[ 1 ] ] == 1

    def move( self, food, grid ):
        headBlob = self.blobs[ 0 ]
        if self.direction == 'U':
            headBlob = (headBlob[ 0 ] , headBlob[ 1 ] - 1)
        elif self.direction == 'D':
            headBlob = (headBlob[ 0 ] , headBlob[ 1 ] + 1)
        elif self.direction == 'L':
            headBlob = (headBlob[ 0 ] - 1 , headBlob[ 1 ])
        elif self.direction == 'R':
            headBlob = (headBlob[ 0 ] + 1 , headBlob[ 1 ])

        if not self.didCollide(headBlob, grid):
            self.followUp ()
            self.remaining_moves = self.remaining_moves - 1
            self.total_moves = min(self.total_moves + 1,500)
            self.blobs[ 0 ] = headBlob

            grid[ self.trail[ 0 ] ][ self.trail[ 1 ] ] = 0
            grid[ headBlob[0] ][ headBlob[1] ] = 1
            got_food = False
            if headBlob[0] == food.x and headBlob[1] == food.y:
                self.grow()
                got_food = True
                grid[ self.trail[ 0 ] ][ self.trail[ 1 ] ] = 1
                food.relocate(grid)
            return food,grid,"ALIVE",got_food
        else:
            #print('Collission')
            return None,grid,"DEAD",False

    def setDirection( self, direction ):
        self.direction = direction
    def getDirection( self ):
        return self.direction

    def updateDirection( self, newDirection ):
        if newDirection == 'U' and self.getDirection() != 'D': self.setDirection('U')
        elif newDirection == 'D' and self.getDirection() != 'U': self.setDirection('D')
        elif newDirection == 'L' and self.getDirection() != 'R': self.setDirection('L')
        elif newDirection == 'R' and self.getDirection() != 'L': self.setDirection('R')
