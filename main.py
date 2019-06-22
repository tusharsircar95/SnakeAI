import pygame
import numpy as np
from pyeasyga import pyeasyga
import random
from SnakeAI.Game import Game
from SnakeAI.GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt


np.random.seed(1000)
game = Game(PLAYAREA_DIMS=(12,12),BORDER_DIMS=(1,3,1,1),
            n_obstacles=0,
            auto_start=True)
ga = GeneticAlgorithm(game=game,n_weights=4,generations=10,population_size=30,
                mutation_probability=0.05,
                crossover_probability=0.50,
                elite_parents=10)
ga.run()

best_individual = gnn.best_individual
print(best_individual)

# np.save('best_individual.npy',best_individual)
best_individual = np.load('best_individual.npy')

game.auto_start = False
game.n_obstacles = 0
game.set_controller(ga.convert_individual_to_game_controller(best_individual))
print(game.play())

