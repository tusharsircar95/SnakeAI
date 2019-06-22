import pyeasyga
import numpy as np
import queue
import copy


class GeneticAlgorithm:
    def __init__(self,game,n_weights,population_size=2,generations=2,
                 crossover_probability=0.70,elite_parents=10,mutation_probability=0.05):
        self.game = game
        self.n_weights = n_weights
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elite_parents = elite_parents
        self.best_individual = None
        self.best_fitness = 0
        self.best_fitness_points = 0
        self.history = {}

    def get_random_weight(self):
        return np.random.choice(np.arange(-50,50,1.0))


    def create_individual(self):
        return [self.get_random_weight() for _ in range(self.n_weights)]

    def cross_over(self,parent1,parent2,mode=0):
        individual = parent1.copy()
        if mode == 0:
            for i in range(len(parent1)):
                if np.random.random() < self.crossover_probability:
                    individual[i] = parent2[i]
        elif mode == 1:
            n = int(len(parent1)/2)#int(np.random.random()*len(parent1))
            individual[:n] = parent2[:n]
        elif mode == 2:
            for i in range(len(parent1)):
                if np.random.random() < self.crossover_probability:
                    individual[i] = (parent1[i]+parent2[i])/2.0
        return individual

    def mutate(self,individual):
        individual = individual.copy()
        for i in range(len(individual)):
            if np.random.random() < self.mutation_probability:
                individual[i] = self.get_random_weight()
        return individual

    def convert_individual_to_game_controller(self, individual):
        def controller(snake,food,grid):
            headBlob = snake.blobs[0]
            directions = [(0,-1),(-1,0),(1,0),(0,1)]
            direction_codes = ['U','L','R','D']
            future_fitness = []
            reaches = []
            for index,direction in enumerate(directions):
                if direction_codes[index] == 'U' and snake.getDirection() == 'D':
                    future_fitness.append(-np.inf)
                    continue
                elif direction_codes[index] == 'D' and snake.getDirection() == 'U':
                    future_fitness.append(-np.inf)
                    continue
                elif direction_codes[index] == 'L' and snake.getDirection() == 'R':
                    future_fitness.append(-np.inf)
                    continue
                elif direction_codes[index] == 'R' and snake.getDirection() == 'L':
                    future_fitness.append(-np.inf)
                    continue

                updated_headBlob = [headBlob[0]+direction[0],headBlob[1]+direction[1]]
                def distance_to_crash(snake,grid,direction):
                    distance = 1
                    while(not snake.didCollide([updated_headBlob[0]+distance*direction[0],updated_headBlob[1]+distance*direction[1]],grid)):
                        distance = distance + 1
                    #distance = min(distance,5)
                    if direction[0] != 0:
                        return (distance-1.0)/grid.shape[0]
                    else: return (distance-1.0)/grid.shape[1]

                def reachable_points(snake,grid):
                    if snake.didCollide(updated_headBlob,grid):
                        reaches.append(-1)
                        return 0
                    reachable_points = 0
                    q = queue.Queue()
                    visited = np.zeros(grid.shape)
                    q.put(updated_headBlob)
                    visited[updated_headBlob[0]][updated_headBlob[1]] = 1
                    while(not q.empty()):
                        current = q.get()
                        for d in directions:
                            new_pos = (current[0]+d[0],current[1]+d[1])

                            if new_pos[0] >= 0 and new_pos[0] < grid.shape[0]:
                                if new_pos[1] >= 0 and new_pos[1] < grid.shape[1]:
                                    if not visited[new_pos[0]][new_pos[1]]:
                                        if not grid[new_pos[0]][new_pos[1]] or (new_pos[0]==snake.blobs[-1][0] and new_pos[1]==snake.blobs[-1][1]):
                                            q.put(new_pos)
                                            visited[new_pos[0]][new_pos[1]] = 1
                                            reachable_points = reachable_points + 1
                    reaches.append(reachable_points)
                    return float(reachable_points)/float(grid.shape[0]*grid.shape[1]-len(snake.blobs))


                def get_fitness(snake,grid):
                    fitness = individual[0]*(-(abs(headBlob[0]-food.x)+abs(headBlob[1]-food.y))+(abs(updated_headBlob[0]-food.x)+abs(updated_headBlob[1]-food.y)))+\
                    individual[1]*(0 if not snake.didCollide(updated_headBlob,grid) else 1)+\
                    (individual[2]*distance_to_crash(snake,grid,(0,-1)))+\
                    (individual[2]*distance_to_crash(snake, grid, (-1, 0)))+\
                    (individual[2]*distance_to_crash(snake, grid, (1, 0)))+\
                    (individual[2]*distance_to_crash(snake, grid, (0, 1)))+\
                    (individual[3]*reachable_points(snake,grid))
                    return fitness
                future_fitness.append(get_fitness(snake,grid))
            decision = direction_codes[np.argmax(future_fitness)]
            #print(reaches, decision)
            #print(future_fitness)
            #print(decision)
            return decision

        return controller

    def calculate_fitness(self,n,index,individual):
        print(individual)
        controller = self.convert_individual_to_game_controller(individual)
        self.game.set_controller(controller)
        fitness_arr = []
        points_arr = []
        for i in range(3):
            points, moves = self.game.play(gnn_info={'gen':n,'n':index,'best_fitness':self.best_fitness,'best_fitness_points':self.best_fitness_points})
            fitness_arr.append(points - 0.05*moves)
            points_arr.append(points)
        fitness = np.mean(fitness_arr)
        points = np.mean(points_arr)
        print(fitness,points)
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_fitness_points = points
            self.best_individual = individual
        return fitness

    def next_generation(self,prev_generation=None,fitness=None):
        if prev_generation is None:
            return np.array([self.create_individual() for _ in range(self.population_size)])
        print('New generation via GA...')

        fitness = fitness - np.min(fitness)
        fitness_normalized = (fitness) / np.sum((fitness))

        elites = []
        generation = []
        fitness_normalized_copy = fitness_normalized.copy()
        for _ in range(self.elite_parents):
            index = np.argmax(fitness_normalized)
            elites.append(prev_generation[index])
            generation.append(prev_generation[index])
            fitness_normalized[index] = -100000

        for _ in range(self.population_size-self.elite_parents):
            index1, index2 = np.random.choice(len(fitness_normalized),size=2,replace=False,p=fitness_normalized_copy)
            child = self.mutate(self.cross_over(prev_generation[index1],prev_generation[index2],mode=0))
            generation.append(child)

        return np.array(generation)

    def run(self):
        prev_generation = None
        fitness = None
        self.best_individual = None
        self.best_fitness = 0
        for n in range(self.generations):
            prev_generation = self.next_generation(prev_generation,fitness)
            fitness = np.array([1e-10 + self.calculate_fitness(n,index,individual) for index,individual in enumerate(prev_generation)])
            self.history[n] = fitness
            print("Generation %d\nBest Fitness: %d\n"%(n,np.max(fitness)))
