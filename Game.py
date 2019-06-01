import pygame
import numpy as np
from pyeasyga import pyeasyga
import random
from SnakeAI.Snake import Snake
from SnakeAI.Food import Food
from SnakeAI.Renderer import Renderer


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
