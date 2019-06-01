import pygame
import numpy as np
from pyeasyga import pyeasyga
import random
from SnakeAI.Game import Game


def sample_controller(snake,food,grid):
    options = ['U','D','L','R']
    return options[np.random.randint(4)]


game = Game(SCREEN_DIMS=(30,30))
game.set_controller(sample_controller)
game.play()



