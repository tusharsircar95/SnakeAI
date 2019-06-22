# Snake.AI

From scratch implementation of genetic algorithm to play the game of snake.
The game interface has been developed in PyGame.


### The Game
The snake has to move through the allotted area without colliding with obstacles, walls or itself.
Eating food (white squares) fetches points and makes the snake grow bigger.
Aim is to collect as many points as possible.
The snake can move in 4 directions: U (UP), D (DOWN), L (LEFT), R (RIGHT)

The following results were achieved by training 10 generations with population size of 30, cross_over probability set to 0.50 , mutation probability set to 0.05 and elite parents set to 10


<table>
  <tr>
    <th>BEST INDIVIDUAL GAMEPLAY</th>
    <th>Mean Generation Fitness VS Generation Number</th>
  <tr>
    <td><img src="https://github.com/tusharsircar95/SnakeAI/blob/master/images/best_individual_gameplay.gif" width="400px"/></td>
    <td><img src="https://github.com/tusharsircar95/SnakeAI/blob/master/images/mean_fitness_plot.png" width="400px"/></td>
  </tr>
</table>

## IMPLEMENTATION DETAILS

### Decision Making
At each step, the snake has 3 possible directions it can choose from:
<ul>
  <li>Keep going straight</li>
  <li>Turn left</li>
  <li>Turn right</li>
</ul>
Depending on which direction the snake is presently moving in, these can be mapped to U, D, L or R.

For each direction, the snake calculates the future state and evaluates its goodness with a heuristic function defined below.


H = w<sub>1</sub> * (Difference in Manhattan Distance from the food) + 

w<sub>2</sub> * (Sum of distances to the nearest obstacle in all directions) + 

w<sub>3</sub> * (Number of Reachable Cells) + 

w<sub>4</sub> * (Does the snake collide with an obstacle)


The snake selects the direction which maximises a heuristic function.
The weights w<sub>i</sub> are selected using genetic algorithm.
Note that each of these values normalized to (0,1) or (-1,1) for uniformity across PLAYAREA_DIMS.

### Genetic Algorithm

Genetic algorithm is an optimization algorithm that simulates the process of natural selection to select the fittest individual(optima). More details can be found <a href="https://www.geeksforgeeks.org/genetic-algorithms/">here</a>

#### INDIVIDUALS
Individuals are weights that define the heuristic function
Each weight is set to a random number in the range [-50,50] with 1.0 precision

#### FITNESS
Fitness is calculated as follows:
Fitness(F) = Number_Of_Food_Items_Eaten - λ  * Steps_Taken

Hence, a snake that is able to maximise the number of food items eaten with the minimum number of steps, is considered more fit to reproduce.
Steps_Taken is added since it penalizes snakes that keep moving in circles.

Additionally, each snake is given 100 moves at the start. Each food item eaten adds 100 points (upto a maximum of 500). If the number of available moves drops below 0, the game ends.
Game also end if the snake collides with an obstacle.

#### SELECTION (Creating a new generation)
We select the top <elite_parents> snakes to be part of the next generation. Moreover, pairs of snakes are sampled with bias (with replacement) based on the fitness scores and then crossed-over.

#### CROSS-OVER (Between parent1 and parent2)
With <crossover_probability>, each weight is set to be the corresponding weight of parent<sub>2</sub>. Rest of the weights are taken from parent<sub>1</sub>

#### MUTATION (Of an individual)
With <mutation_probability>, each weight is set to be new random number

## USAGE

### Creating A Game Object

```
game = Game( PLAYAREA_DIMS=(12,12),
            BORDER_DIMS=(1,3,1,1),
            GRID_SQ=20,
            CONTROLLER=None,
            auto_start=False,
            n_obstacles=0)
game.play()
```
<ul>
  <li><b>PLAYAREA_DIMS:</b> Dimension of area where snake is allowed to move</li>

  <li><b>BORDER_DIMS:</b> Left, top, right and bottom border size</li>

  <li><b>GRID_SQ:</b> Each of the above dimensions represent a square of side length <GRID_SQ></li>
  <li><b>CONTROLLER:</b> Function that takes a information about the snake, obstacles and food object and decides which direction to move in. If None, snake is controller via arrow keys manually</li>
  <li><b>auto_start:</b> Whether the game starts automatically on calling play(). If False, press P to start the game</li>
  <li><b>n_obstacles:</b> Number of obstacles placed randomly within the grid</li>
</ul>

Note that position of the snake or food object are all defined in terms of PLAY_AREA_DIMS and not the actual pixel co-ordinates of the game window

### Creating A Genetic Algorithm Object

```
ga = GeneticAlgorithm(game,
                  n_weights,
                  population_size=10,
                  generations=30,
                  crossover_probability=0.70,
                  elite_parents=10,
                  mutation_probability=0.05)
ga.run()

# Get the best individual after training
print(ga.best_individual)

# Get average fitness per generation
for n in range(n_generations):
    print(n,np.mean(ga.history[n]))

# See the best individual in action
game.auto_start = False
game.set_controller(ga.convert_individual_to_game_controller(ga.best_individual))
print(game.play())

```
<ul>
  <li><b>game:</b> Game object that can be called to evaluate fitness of an individual</li>
  <li><b>n_weights:</b> Number of weight parameters required to define the heuristic function</li>
  <li><b>population_size:</b> Number of individuals in each generation</li>
  <li><b>generations:</b> Number of generations</li>
  <li><b>crossover_probability:</b> Probability of exchanging weights while generating new individual from two parents</li>
  <li><b>mutation_probability:</b> Probability of randomly changing one of the weights of an individual</li>
  <li><b>elite_parents:</b> Number of top individuals that are retained for the next generation</li>
</ul>

### Defining Your Custom Controller & Fitness Criteria

```
# Takes as input information about the grid area (where obstacles are present), snake object and food object
# Returns a direction 'L', 'R', 'U' or 'D'
def controller(snake,food,grid):
  pass
```
The following are useful information that can be utilized to define the controller logic:
<ul>
  <li><b>snake.blobs[]:</b> List of tuples with co-ordinates of all the snake squares. snake.blobs[0] contains the position of the snake head</li>
  <li><b>grid:</b> 2D boolean array. Indicates whether a grid cell is empty or not. Empty means that there is no obstacle and no snake blob at that position</li>
  <li><b>snake.getDirection():</b> Direction in which the snake is moving currently</li>
  <li><b>snake.didCollide(position,grid):</b> Whether the snake will collide at the given position</li>
  <li><b>food.x and food.y:</b> Co-ordinates of the food object on the grid</li>
</ul>


##### NOTE:
One alternate way to formulate the problem was as follows. At each step, based on position of snake, food and obstacles, features are extracted and passed to a neural network / logistic regression function. The function outputs the direction where the snake should move. Weights of the network could be trained by GA.

I was able to get this to work but was only able to learn a simple function that moves towards the food but avoids an obstacle if it is in front of it. This works to some extent but obviously fails in the long run as it ends up getting into dead ends.

Probably, bigger population size and generations would have helped.

## References
<ol>
  <li><a href="https://www.geeksforgeeks.org/genetic-algorithms/">GeeksForGeeks</a></li>
  <li><a href="https://github.com/han-gyeol/Genetic-Algorithm-Snake">Genetic Algorithm Snake</a></li>
</ol>
