# Snake.AI

From scratch implementation of genetic algorithm to train a logistic regression model to play the game of snake
The game interface has been developed in PyGame.

## Implementation Details

### The Game
The snake has to move through the allotted area without colliding with obstacles, walls or itself.
Eating food (white squares) fetches points and makes the snake grow bigger.
Aim is to collect as many points as possible.
The snake can move in 4 directions: U (UP), D (DOWN), L (LEFT), R (RIGHT)


### Controller and Features
Features refer to information available to the snake at any point.
A Controller function maps a set of features to the direction it wants the snake to move in

The following features have been used. Note that these are calculated in reference to the direction the snake is moving in and the snake head position at the time of calculation.
<ul>
<li>food_front : 1 if food is in the direction of movement, -1 if it's in the opposite direction and 0 if it's at the same level as the snake head</li>
<li>food_left : 1 if food is left of the snake and -1 otherwise</li>
<li>food_right : 1 if food is right of the snake and -1 otherwise</li>
<li>front_free : 1 if the space ahead of the snake is not blocked and -1 otherwise</i>
<li>left_free : 1 if the space left of the snake is not blocked and -1 otherwise</li>
<li>right_free : 1 if the space right of the snake is not blocked and -1 otherwise</li>

These 6 features are can be passed through a neural network / logistic regression model to generate probabilities of movement in either TURN-LEFT, TURN-RIGHT or GO-STRAIGHT direction. These are mapped to L, R, D and U depending on the present direction of the snake.

### Genetic Algorithm

Genetic algorithm is an optimization algorithm that simulates the process of natural selection to select the fittest individual(optima). More details can be found <a href="https://www.geeksforgeeks.org/genetic-algorithms/">here</a>

#### INDIVIDUALS
Individuals are weights of the network that map features to a movement direction.
Each weight is set to a random integer in the range [-3,3]

#### FITNESS
Fitness is calculated as follows:
<ul>
  <li>Eats Food: +30</li>
  <li>Moves closer to food: +1</li>
  <li>Moves away from food: -1.5</li>
  <li>Collides: -20</li>
</ul>

Note that we give less points to move towards food than we take subtract for moving away otherwise the snake may move in a loop indefinitely without losing any fitness.
Also, we end the game if the fitness reaches below -50, to penalize snakes that move over the grid without prioritizing food.

#### SELECTION (Creating a new generation)
We select the top <elite_parents> snakes to be part of the next generation. Moreover, pairs of snakes are sampled with bias (with replacement) based on the fitness scores and then crossed-over.

#### CROSS-OVER (Between parent1 and parent2)
With <crossover_probability>, each weight is set to be the average weight of the two parents. Rest of the weights are taken from parent1

#### MUTATION (Of an individual)
With <mutation_probability>, each weight is set to be new random number


