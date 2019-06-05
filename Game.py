import pygame
import numpy as np
from pyeasyga import pyeasyga
import random
from SnakeAI.Snake import Snake
from SnakeAI.Food import Food
from SnakeAI.Renderer import Renderer


class Game:

    def __init__(self,SCREEN_DIMS=(40,40),GRID_SQ=20,CONTROLLER=None,auto_start=False):
        pygame.init()
        self.SCREEN_DIMS = SCREEN_DIMS
        self.GRID_SQ = GRID_SQ
        self.GRID = np.zeros(SCREEN_DIMS)
        self.SCORE = 0
        self.STATE = "NOT_STARTED"
        self.SNAKE = Snake(self.GRID)
        self.FOOD = Food()
        self.FOOD.relocate(self.GRID)
        self.CONTROLLER = CONTROLLER
        self.FONT = pygame.font.SysFont("comicsansms", 30)
        self.GRID = self.SNAKE.updateGrid(self.GRID)
        self.auto_start = auto_start
        self.obstacles = []

    def setObstacles(self,n):
        self.obstacles = []
        for i in range(n):
            x = self.SNAKE.blobs[0][0]
            y = self.SNAKE.blobs[0][1]
            while self.GRID[x][y] != 0:
                x = np.random.randint(self.SCREEN_DIMS[0])
                y = np.random.randint(self.SCREEN_DIMS[1])
            self.GRID[x][y] = 1.0
            self.obstacles.append((x,y))

    def reset_game(self):
        self.GRID = np.zeros(self.SCREEN_DIMS)
        self.SCORE = 0
        self.STATE = "NOT_STARTED"
        self.SNAKE = Snake(self.GRID)
        self.FOOD = Food()
        self.FOOD.relocate(self.GRID)
        self.GRID = self.SNAKE.updateGrid(self.GRID)
        self.setObstacles(10)

    def set_controller(self,controller):
        self.CONTROLLER = controller

    def play(self,auto_start=False):
        self.reset_game()
        renderer = Renderer(SCREEN_DIMS=self.SCREEN_DIMS,
                            GRID_SQ=self.GRID_SQ,
                            FONT=self.FONT)

        screen = pygame.display.set_mode((self.SCREEN_DIMS[0] * self.GRID_SQ,
                                          self.SCREEN_DIMS[1] * self.GRID_SQ))
        quitGame = False
        text_gameover = renderer.FONT.render("Game Over", True, (0, 255, 0))
        clock = pygame.time.Clock()

        if self.auto_start:
            self.STATE = 'ALIVE'
        towards_food_streak = 0
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
            renderer.render_obstacles(screen,self.obstacles)
            if self.STATE == "DEAD":
                renderer.render_game_over(screen, text_gameover)
                self.SCORE = self.SCORE - 20
                quitGame = True
            elif self.SCORE < -50:
                self.STATE = "DEAD"
                quitGame = True
            elif self.STATE == "ALIVE":
                old_position = self.SNAKE.blobs[0]
                self.FOOD, self.GRID, self.STATE, got_food = self.SNAKE.move(self.FOOD, self.GRID)
                new_position = self.SNAKE.blobs[0]
                if got_food:
                    self.SCORE = self.SCORE + 30
                #self.SCORE = self.SCORE - 1
                #self.SCORE = self.SCORE - 30
                if True and self.FOOD is not None:
                    if abs(old_position[0]-self.FOOD.x) + abs(old_position[1]-self.FOOD.y) > abs(new_position[0]-self.FOOD.x) + abs(new_position[1]-self.FOOD.y) :
                        if towards_food_streak <= 0:
                            towards_food_streak = 1
                        else: towards_food_streak = towards_food_streak + 1
                        self.SCORE = self.SCORE + 1.00 * 1.0
                    else:
                        if towards_food_streak >= 0:
                            towards_food_streak = -1
                        else: towards_food_streak = towards_food_streak - 1
                        self.SCORE = self.SCORE + 1.50 * -1.0

            # for i in range(self.SCREEN_DIMS[0]):
            #     for j in range(self.SCREEN_DIMS[1]):
            #         if self.GRID[i][j] == 1:
            #             print(i,j)

            pygame.display.flip()
            clock.tick(180)

        #print('Score: %d' % self.SCORE)
        # pygame.quit()
        return self.SCORE
