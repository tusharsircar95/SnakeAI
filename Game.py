import pygame
import numpy as np
from pyeasyga import pyeasyga
import random
from SnakeAI.Snake import Snake
from SnakeAI.Food import Food
from SnakeAI.Renderer import Renderer


class Game:

    def __init__(self,PLAYAREA_DIMS=(12,12),BORDER_DIMS=(1,3,1,1),GRID_SQ=20,CONTROLLER=None,auto_start=False,n_obstacles=0):
        pygame.init()
        self.PLAYAREA_DIMS = PLAYAREA_DIMS
        self.BORDER_DIMS = BORDER_DIMS
        self.SCREEN_DIMS = (self.PLAYAREA_DIMS[0]+BORDER_DIMS[0]+BORDER_DIMS[2], self.PLAYAREA_DIMS[1]+BORDER_DIMS[1]+BORDER_DIMS[3])
        self.GRID_SQ = GRID_SQ
        self.GRID = np.zeros(PLAYAREA_DIMS)
        self.FOODS_EATEN = 0
        self.STATE = "NOT_STARTED"
        self.SNAKE = Snake(self.GRID)
        self.FOOD = Food()
        self.FOOD.relocate(self.GRID)
        self.CONTROLLER = CONTROLLER
        self.FONT = pygame.font.SysFont("comicsansms", 22)
        self.GRID = self.SNAKE.updateGrid(self.GRID)
        self.auto_start = auto_start
        self.obstacles = []
        self.n_obstacles = n_obstacles
        self.gnn_info = {}

    def setObstacles(self,n):
        self.obstacles = []
        for i in range(n):
            x = self.SNAKE.blobs[0][0]
            y = self.SNAKE.blobs[0][1]
            while self.GRID[x][y] != 0:
                x = np.random.randint(self.PLAYAREA_DIMS[0])
                y = np.random.randint(self.PLAYAREA_DIMS[1])
            self.GRID[x][y] = 1.0
            self.obstacles.append((x,y))

    def reset_game(self):
        self.GRID = np.zeros(self.PLAYAREA_DIMS)
        self.FOODS_EATEN = 0
        self.STATE = "NOT_STARTED"
        self.SNAKE = Snake(self.GRID)
        self.FOOD = Food()
        self.FOOD.relocate(self.GRID)
        self.GRID = self.SNAKE.updateGrid(self.GRID)
        self.setObstacles(self.n_obstacles)

    def set_controller(self,controller):
        self.CONTROLLER = controller

    def play(self,gnn_info={}):
        self.reset_game()
        _image_num = 0

        self.gnn_info = gnn_info
        renderer = Renderer(SCREEN_DIMS=self.SCREEN_DIMS,
                            BORDERS=self.BORDER_DIMS,
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

            str_num = "000" + str(_image_num)
            file_name = "image" + str_num[-4:] + ".jpg"
            pygame.image.save(screen, "SnakeAI/images/pygame_video/" + file_name)
            _image_num += 1


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
            renderer.render_borders(screen)
            renderer.render_snake(screen, self.SNAKE)
            renderer.render_food(screen, self.FOOD)
            renderer.render_score(screen, self.FOODS_EATEN)
            renderer.render_gnn_info(screen, self.gnn_info)
            renderer.render_obstacles(screen,self.obstacles)
            if self.STATE == "DEAD":
                renderer.render_game_over(screen, text_gameover)
                quitGame = True
            elif self.SNAKE.remaining_moves < 0:
                self.STATE = "DEAD"
                quitGame = True
            elif self.STATE == "ALIVE":
                self.FOOD, self.GRID, self.STATE, got_food = self.SNAKE.move(self.FOOD, self.GRID)
                if got_food:
                    self.FOODS_EATEN = self.FOODS_EATEN + 1

            pygame.display.flip()
            clock.tick(180)

        return self.FOODS_EATEN, self.SNAKE.total_moves
