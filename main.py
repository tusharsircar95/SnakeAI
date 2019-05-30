import pygame
import numpy as np

class GameObjects:

    @staticmethod
    def init(SCREEN_DIMS=(40,40),GRID_SQ=20,CONTROLLER=None):
        GameObjects.SCREEN_DIMS = SCREEN_DIMS
        GameObjects.GRID_SQ = GRID_SQ
        GameObjects.GRID = np.zeros(SCREEN_DIMS)
        GameObjects.SCORE = 0
        GameObjects.STATE = "NOT_STARTED"
        GameObjects.SNAKE = Snake ()
        GameObjects.FOOD = Food ()
        GameObjects.CONTROLLER = CONTROLLER
        GameObjects.FONT = pygame.font.SysFont ( "comicsansms" , 30 )

class Snake:
    def __init__(self):
        origin = int(GameObjects.SCREEN_DIMS[0]/2)
        self.direction = 'R'
        self.blobs = []
        for i in range(3):
            self.blobs.append((origin-i,origin))
            GameObjects.GRID[origin-i][origin] = 1
        self.trail = None

    def followUp( self ):
        self.trail = self.blobs[-1]
        for i in range(len(self.blobs)-1,0,-1):
            self.blobs[i] = self.blobs[i-1]

    def grow( self ):
        self.blobs.append(self.trail)

    def didCollide( self, headBlob ):
        if headBlob[0] < 0 or headBlob[0] >= GameObjects.SCREEN_DIMS[0]:
            print('Side wall collission')
            return True
        if headBlob[1] < 0 or headBlob[1] >= GameObjects.SCREEN_DIMS[1]:
            print ( 'TopBottom wall collission' )
            return True
        if GameObjects.GRID[ headBlob[ 0 ] ][ headBlob[ 1 ] ] == 1:
            print ( 'Self collission' )
        return GameObjects.GRID[headBlob[0]][headBlob[1]] == 1

    def move( self, food ):
        headBlob = self.blobs[ 0 ]
        if self.direction == 'U':
            headBlob = (headBlob[ 0 ] , headBlob[ 1 ] - 1)
        elif self.direction == 'D':
            headBlob = (headBlob[ 0 ] , headBlob[ 1 ] + 1)
        elif self.direction == 'L':
            headBlob = (headBlob[ 0 ] - 1 , headBlob[ 1 ])
        elif self.direction == 'R':
            headBlob = (headBlob[ 0 ] + 1 , headBlob[ 1 ])

        if not self.didCollide(headBlob):
            self.followUp ()
            self.blobs[ 0 ] = headBlob

            GameObjects.GRID[ self.trail[ 0 ] ][ self.trail[ 1 ] ] = 0
            GameObjects.GRID[ headBlob[0] ][ headBlob[1] ] = 1
            if headBlob[0] == food.x and headBlob[1] == food.y:
                self.grow()
                GameObjects.SCORE = GameObjects.SCORE + 1
                GameObjects.GRID[ self.trail[ 0 ] ][ self.trail[ 1 ] ] = 1
                food.relocate()
            return food,"ALIVE"
        else:
            print('Collission:',headBlob,self.blobs[0])
            return None,"DEAD"

    def setDirection( self, direction ):
        self.direction = direction
        print(self.direction)
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

    def relocate( self ):
        while GameObjects.GRID[self.x][self.y] != 0:
            self.x = int(np.random.random() * GameObjects.SCREEN_DIMS[0])
            self.y = int(np.random.random() * GameObjects.SCREEN_DIMS[1])


class Renderer:
    def __init__(self):
        pass
    @staticmethod
    def render_snake ( screen , snake ):
        for index,blob in enumerate(snake.blobs):
            pygame.draw.rect ( screen ,
                               (np.random.random () * 255 , np.random.random () * 255 , np.random.random () * 255) ,
                               pygame.Rect ( blob[ 0 ] * GameObjects.GRID_SQ , blob[ 1 ] * GameObjects.GRID_SQ ,
                                             GameObjects.GRID_SQ , GameObjects.GRID_SQ ) )

    @staticmethod
    def render_food ( screen , food ):
        if food is None:
            return
        pygame.draw.rect ( screen , (255 , 255 , 255) ,
                           pygame.Rect ( food.x * GameObjects.GRID_SQ , food.y * GameObjects.GRID_SQ ,
                                         GameObjects.GRID_SQ , GameObjects.GRID_SQ ) )

    @staticmethod
    def render_game_over( screen, text ):
        screen.blit ( text ,
                      ( (GameObjects.SCREEN_DIMS[ 0 ] * GameObjects.GRID_SQ / 2 - text.get_width () // 2) ,
                        (GameObjects.SCREEN_DIMS[ 1 ] * GameObjects.GRID_SQ/ 2 - text.get_height ()) ))
    @staticmethod
    def render_score(screen, score):
        text_score = GameObjects.FONT.render ( str(score) , True , (0 , 255 , 0) )
        screen.blit ( text_score ,
                      ((0.95*GameObjects.SCREEN_DIMS[ 0 ] * GameObjects.GRID_SQ - text_score.get_width () // 2) ,
                       (2 * GameObjects.GRID_SQ - text_score.get_height ())) )


def sample_controller(snake,food,grid):
    options = ['U','D','L','R']
    return options[np.random.randint(4)]




def play():
    pygame.init ()
    GameObjects.init ( CONTROLLER=None )
    screen = pygame.display.set_mode ( (GameObjects.SCREEN_DIMS[ 0 ] * GameObjects.GRID_SQ ,
                                        GameObjects.SCREEN_DIMS[ 1 ] * GameObjects.GRID_SQ) )
    quitGame = False
    text_gameover = GameObjects.FONT.render ( "Game Over" , True , (0 , 255 , 0) )
    text_score = GameObjects.FONT.render ( "0" , True , (0 , 255 , 0) )
    clock = pygame.time.Clock ()


    while not quitGame:

        '''
        features = f ( snake, GameObject.GRID, food )
        action = g ( features )
        doAction (action)
        '''
        print('New Frame')
        events = pygame.event.get()
        # Handle general events
        for event in events:
            if event.type == pygame.QUIT:
                quitGame = True
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                        GameObjects.init()
                        print('Restarting...')

                if event.key == pygame.K_p:
                    if GameObjects.STATE != "DEAD":
                        GameObjects.STATE = "ALIVE"

        # Game controls
        if GameObjects.STATE == 'ALIVE':
            newDirection = GameObjects.SNAKE.getDirection ()

            if GameObjects.CONTROLLER is None:
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
                GameObjects.SNAKE.updateDirection ( newDirection )
            elif callable(GameObjects.CONTROLLER):
                newDirection = GameObjects.CONTROLLER(GameObjects.SNAKE,GameObjects.FOOD,GameObjects.GRID)
                GameObjects.SNAKE.updateDirection ( newDirection )


        # Graphics rendering
        screen.fill((0,0,0))
        Renderer.render_snake ( screen , GameObjects.SNAKE )
        Renderer.render_food(screen,GameObjects.FOOD)
        Renderer.render_score ( screen , GameObjects.SCORE )

        if GameObjects.STATE == "ALIVE":
            GameObjects.FOOD,GameObjects.STATE = GameObjects.SNAKE.move(GameObjects.FOOD)
        elif GameObjects.STATE == "DEAD":
            print(np.sum(GameObjects.GRID))
            Renderer.render_game_over(screen,text_gameover)
            quitGame = True
        # for i in range(GameObjects.SCREEN_DIMS[0]):
        #     for j in range(GameObjects.SCREEN_DIMS[1]):
        #         if GameObjects.GRID[i][j] == 1:
        #             print(i,j)

        pygame.display.flip ()
        clock.tick ( 40 )

    print('Score: %d'%GameObjects.SCORE)
    #pygame.quit()
    return GameObjects.SCORE

