import pygame
import numpy as np
from pyeasyga import pyeasyga
import random


class Snake:
    def __init__(self,grid):
        origin = int(grid.shape[0]/2)
        self.direction = 'R'
        self.blobs = []
        for i in range(3):
            self.blobs.append((origin-i,origin))
        self.trail = None

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

    def didCollide( self, headBlob, grid ):
        if headBlob[0] < 0 or headBlob[0] >= grid.shape[0]:
            print('Side wall collission')
            return True
        if headBlob[1] < 0 or headBlob[1] >= grid.shape[1]:
            print ( 'TopBottom wall collission' )
            return True
        if grid[ headBlob[ 0 ] ][ headBlob[ 1 ] ] == 1:
            print ( 'Self collission' )
        return grid[ headBlob[ 0 ] ][ headBlob[ 1 ] ] == 1

    def move( self, food, grid, score ):
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
            self.blobs[ 0 ] = headBlob

            grid[ self.trail[ 0 ] ][ self.trail[ 1 ] ] = 0
            grid[ headBlob[0] ][ headBlob[1] ] = 1
            if headBlob[0] == food.x and headBlob[1] == food.y:
                self.grow()
                score = score + 1
                grid[ self.trail[ 0 ] ][ self.trail[ 1 ] ] = 1
                food.relocate(grid)
            return food,grid,"ALIVE",score
        else:
            print('Collission:',headBlob,self.blobs[0])
            return None,grid,"DEAD", score

    def setDirection( self, direction ):
        self.direction = direction
    def getDirection( self ):
        return self.direction

    def updateDirection( self, newDirection ):
        if newDirection == 'U' and self.getDirection() != 'D': self.setDirection('U')
        elif newDirection == 'D' and self.getDirection() != 'U': self.setDirection('D')
        elif newDirection == 'L' and self.getDirection() != 'R': self.setDirection('L')
        elif newDirection == 'R' and self.getDirection() != 'L': self.setDirection('R')


class Food:
    def __init__(self):
        self.x = 2 * 1
        self.y = 2 * 1

    def relocate( self, grid ):
        while grid[self.x][self.y] != 0:
            self.x = int(np.random.random() * grid.shape[0])
            self.y = int(np.random.random() * grid.shape[1])


class Renderer:
    def __init__(self,SCREEN_DIMS,GRID_SQ,FONT):
        self.SCREEN_DIMS = SCREEN_DIMS
        self.GRID_SQ = GRID_SQ
        self.FONT = FONT

    def render_snake ( self, screen , snake ):
        for index,blob in enumerate(snake.blobs):
            pygame.draw.rect ( screen ,
                               (np.random.random () * 255 , np.random.random () * 255 , np.random.random () * 255) ,
                               pygame.Rect ( blob[ 0 ] * self.GRID_SQ , blob[ 1 ] * self.GRID_SQ ,
                                             self.GRID_SQ , self.GRID_SQ ) )

    def render_food ( self, screen , food ):
        if food is None:
            return
        pygame.draw.rect ( screen , (255 , 255 , 255) ,
                           pygame.Rect ( food.x * self.GRID_SQ , food.y * self.GRID_SQ ,
                                         self.GRID_SQ , self.GRID_SQ ) )

    def render_game_over( self, screen, text ):
        screen.blit ( text ,
                      ( (self.SCREEN_DIMS[ 0 ] * self.GRID_SQ / 2 - text.get_width () // 2) ,
                        (self.SCREEN_DIMS[ 1 ] * self.GRID_SQ/ 2 - text.get_height ()) ))
    def render_score(self, screen, score):
        text_score = self.FONT.render ( str(score) , True , (0 , 255 , 0) )
        screen.blit ( text_score ,
                      ((0.95*self.SCREEN_DIMS[ 0 ] * self.GRID_SQ - text_score.get_width () // 2) ,
                       (2 * self.GRID_SQ - text_score.get_height ())) )


class Game:

    def __init__(self,SCREEN_DIMS=(40,40),GRID_SQ=20,CONTROLLER=None):
        pygame.init()
        self.SCREEN_DIMS = SCREEN_DIMS
        self.GRID_SQ = GRID_SQ
        self.GRID = np.zeros(SCREEN_DIMS)
        self.SCORE = 0
        self.STATE = "NOT_STARTED"
        self.SNAKE = Snake(self.GRID)
        self.FOOD = Food()
        self.CONTROLLER = CONTROLLER
        self.FONT = pygame.font.SysFont("comicsansms", 30)
        self.GRID = self.SNAKE.updateGrid(self.GRID)

    def reset_game(self):
        self.GRID = np.zeros(self.SCREEN_DIMS)
        self.SCORE = 0
        self.STATE = "NOT_STARTED"
        self.SNAKE = Snake(self.GRID)
        self.FOOD = Food()
        self.GRID = self.SNAKE.updateGrid(self.GRID)

    def set_controller(self,controller):
        self.CONTROLLER = controller

    def play(self):
        self.reset_game()
        renderer = Renderer(SCREEN_DIMS=self.SCREEN_DIMS,
                            GRID_SQ=self.GRID_SQ,
                            FONT=self.FONT)

        screen = pygame.display.set_mode((self.SCREEN_DIMS[0] * self.GRID_SQ,
                                          self.SCREEN_DIMS[1] * self.GRID_SQ))
        quitGame = False
        text_gameover = renderer.FONT.render("Game Over", True, (0, 255, 0))
        clock = pygame.time.Clock()

        while not quitGame:

            events = pygame.event.get()
            # Handle general events
            for event in events:
                if event.type == pygame.QUIT:
                    quitGame = True
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        self.reset_game()
                        print('Restarting...')

                    if event.key == pygame.K_p:
                        if self.STATE != "DEAD":
                            self.STATE = "ALIVE"

            # Game controls
            if self.STATE == 'ALIVE':
                newDirection = self.SNAKE.getDirection()

                if self.CONTROLLER is None:
                    for event in events:
                        if event.type == pygame.QUIT:
                            quitGame = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                newDirection = 'U'
                            elif event.key == pygame.K_DOWN:
                                newDirection = 'D'
                            elif event.key == pygame.K_LEFT:
                                newDirection = 'L'
                            elif event.key == pygame.K_RIGHT:
                                newDirection = 'R'
                    self.SNAKE.updateDirection(newDirection)
                elif callable(self.CONTROLLER):
                    newDirection = self.CONTROLLER(self.SNAKE, self.FOOD, self.GRID)
                    self.SNAKE.updateDirection(newDirection)

            # Graphics rendering
            screen.fill((0, 0, 0))
            renderer.render_snake(screen, self.SNAKE)
            renderer.render_food(screen, self.FOOD)
            renderer.render_score(screen, self.SCORE)

            if self.STATE == "ALIVE":
                self.FOOD, self.GRID, self.STATE, self.SCORE = self.SNAKE.move(
                    self.FOOD, self.GRID, self.SCORE)
            elif self.STATE == "DEAD":
                renderer.render_game_over(screen, text_gameover)
                # quitGame = True
            # for i in range(self.SCREEN_DIMS[0]):
            #     for j in range(self.SCREEN_DIMS[1]):
            #         if self.GRID[i][j] == 1:
            #             print(i,j)

            pygame.display.flip()
            clock.tick(180)

        print('Score: %d' % self.SCORE)
        # pygame.quit()
        return self.SCORE


def sample_controller(snake,food,grid):
    options = ['U','D','L','R']
    return options[np.random.randint(4)]


game = Game(SCREEN_DIMS=(30,30))
game.set_controller(sample_controller)
game.play()



