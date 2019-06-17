import pygame
import numpy as np
from pyeasyga import pyeasyga
import random
from SnakeAI.Game import Game
from SnakeAI.GeneticNN import GeneticNN

def sample_controller(snake,food,grid):
    options = ['U','D','L','R']
    return options[np.random.randint(4)]


def to_features_1(snake,food,grid):
    front_free, left_free, right_free = 1.0, 1.0, 1.0
    food_x, food_y = 0.0,0.0
    food_left,food_right,food_front = 0.0,0.0,0.0
    front_wall, left_wall, right_wall = 0.0, 0.0, 0.0
    direction = [0,0]
    headBlob = snake.blobs[0]
    if snake.direction == 'U':
        front_free = 1.0 - snake.didCollide([headBlob[0],headBlob[1]-1],grid)
        left_free = 1.0 - snake.didCollide([headBlob[0]-1,headBlob[1]],grid)
        right_free = 1.0 - snake.didCollide([headBlob[0]+1,headBlob[1]],grid)
        front_wall = headBlob[1] - grid.shape[0]
        left_wall = headBlob[0]
        right_wall = grid.shape[1] - headBlob[0]
        food_x = food.x - headBlob[0]
        food_y = headBlob[1] - food.y
        direction = [0,1]
    elif snake.direction == 'D':
        front_free = 1.0 - snake.didCollide([headBlob[0], headBlob[1] + 1], grid)
        left_free = 1.0 - snake.didCollide([headBlob[0]+1, headBlob[1]], grid)
        right_free = 1.0 - snake.didCollide([headBlob[0]-1, headBlob[1]], grid)
        front_wall = -(headBlob[1] - grid.shape[0])
        right_wall = headBlob[0]
        left_wall = grid.shape[1] - headBlob[0]
        food_x = -(food.x - headBlob[0])
        food_y = -(headBlob[1]-food.y)
        direction = [0, -1]
    elif snake.direction == 'L':
        front_free = 1.0 - snake.didCollide([headBlob[0]-1, headBlob[1]], grid)
        left_free = 1.0 - snake.didCollide([headBlob[0], headBlob[1]+1], grid)
        right_free = 1.0 - snake.didCollide([headBlob[0], headBlob[1]-1], grid)
        front_wall = headBlob[0]
        left_wall = grid.shape[0] - headBlob[1]
        right_wall = headBlob[1]
        food_x = headBlob[1] - food.y
        food_y = -(food.x - headBlob[0])
        direction = [-1, 0]
    elif snake.direction == 'R':
        front_free = 1.0 - snake.didCollide([headBlob[0]+1, headBlob[1]], grid)
        left_free = 1.0 - snake.didCollide([headBlob[0], headBlob[1]-1], grid)
        right_free = 1.0 - snake.didCollide([headBlob[0], headBlob[1]+1], grid)
        front_wall = grid.shape[1] - headBlob[0]
        right_wall = grid.shape[0] - headBlob[1]
        left_wall = headBlob[1]
        food_x = -(headBlob[1] - food.y)
        food_y = (food.x - headBlob[0])
        direction = [1, 0]

    if front_free == 0:
        front_free = -1
    if left_free == 0:
        left_free = -1
    if right_free == 0:
        right_free = -1
    #food_x = food.x - headBlob[0]
    #food_y = food.y - headBlob[1]

    food_norm = 1e-5 + np.max([food_x,food_y])#np.linalg.norm([food_x,food_y])
    food_x = np.sign(food_x)
    food_y = np.sign(food_y)
    food_right = 1 if food_x > 0 else -1
    food_left = 1 if food_x < 0 else -1
    food_front = 1 if food_y > 0 else 0 if food_y == 0 else -1

    return np.array([float(front_free),float(food_front),
                     float(left_free),float(food_left),
                     float(right_free),float(food_right)])


def to_features_2(snake,food,grid):

    headBlob = snake.blobs[0]
    W = grid.shape[0]
    H = grid.shape[1]

    def get_block(grid,origin,direction):
        max_line = 0
        for i in range(1,grid.shape[0]):
            max_line = i
            location = origin + i*direction
            if location[0] < 0 or location[0] >= grid.shape[0] or location[1] < 0 or location[1] >= grid.shape[1]:
                break
            if grid[location[0]][location[1]] == 1.0:
                break
        return float(max_line)

    food_right = max(food.x-headBlob[0],0)
    food_left = max(headBlob[0]-food.x,0)
    food_up = max(headBlob[1]-food.y,0)
    food_down = max(food.y-headBlob[1],0)
    block_left = get_block(grid,np.array(headBlob),np.array([-1,0]))
    block_right = get_block(grid, np.array(headBlob), np.array([1, 0]))
    block_up = get_block(grid, np.array(headBlob), np.array([0, -1]))
    block_down = get_block(grid, np.array(headBlob), np.array([0, 1]))
    block_tl = get_block(grid, np.array(headBlob), np.array([-1, -1]))
    block_tr = get_block(grid, np.array(headBlob), np.array([1, -1]))
    block_bl = get_block(grid, np.array(headBlob), np.array([-1, 1]))
    block_br = get_block(grid, np.array(headBlob), np.array([1, 1]))
    free_left = -1.0 if snake.didCollide([headBlob[0]-1,headBlob[1]],grid) else 1.0
    free_right = -1.0 if snake.didCollide([headBlob[0] + 1, headBlob[1]],grid) else 1.0
    free_up = -1.0 if snake.didCollide([headBlob[0], headBlob[1]-1],grid) else 1.0
    free_down = -1.0 if snake.didCollide([headBlob[0], headBlob[1]+1],grid) else 1.0


    return np.array([float(food_left),float(food_right),float(food_up),float(food_down),
                     float(block_left),float(block_right),float(block_up),float(block_down),
                     float(block_tl),float(block_tr),float(block_bl),float(block_br),
                     float(free_left),float(free_right),float(free_down),float(free_up)])

#     return np.array([float(front_free),float(left_free),float(right_free),
#                      #float(food_x),float(food_y),
#                      float(food_left),float(food_right),float(food_front),
#                      #float(front_wall),float(left_wall),float(right_wall),
# #                     float(direction[0]),float(direction[1])])
#                      ])

# to_features_1 - Info about neighboring points, [6,3], learns to avoid obstacles and move towards food
# But natually fails to see the bigger picture and avoid getting trapped. Requires training with global features
# 1.0 TOWARDS FOOD AND -1.5 AWAW FROM IT
# FOOD GIVES +30, DEATH GIVES -20, NEGATIVE CAP -50
# POP_SIZE 60, GENS 100 MP 0.05

np.random.seed(100000)
game = Game(PLAYAREA_DIMS=(20,20),BORDER_DIMS=(1,3,1,1),
            n_obstacles=20,
            auto_start=True)
#game.play("ASDASDS")
gnn = GeneticNN(game=game,layers=[6,3],to_features=to_features_1,generations=100,population_size=2000,
                mutation_probability=0.05,
                crossover_probability=0.80,
                elite_parents=20)
gnn.run()


