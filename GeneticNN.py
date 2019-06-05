import pyeasyga
import numpy as np



class GeneticNN:
    def __init__(self,game,layers,to_features,population_size=2,generations=2,
                 crossover_probability=0.70,elite_parents=10,mutation_probability=0.05):
        self.game = game
        self.layers = layers
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.to_features = to_features
        self.elite_parents = elite_parents
        self.best_individual = None
        self.best_fitness = 0
        # def to_features(snake,food,grid):
        #     return np.random.random([self.layers[0],1])
        # self.to_features = to_features

    def get_random_weight(self):
        return np.random.randint(-6,6) * 0.5

    def create_individual(self):
        n_params = 0
        for i in range(1,len(self.layers)):
            n_params += self.layers[i]*self.layers[i-1] + self.layers[i]
        return [self.get_random_weight() for _ in range(n_params)]

    def cross_over(self,parent1,parent2,mode=0):
        individual = parent1
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
        for i in range(len(individual)):
            if np.random.random() < self.mutation_probability:
                individual[i] = self.get_random_weight()
        return individual

    def convert_individual_to_game_controller(self, individual):
        def controller(snake,food,grid):
            activation = self.to_features(snake,food,grid).reshape(self.layers[0],1)
            offset = 0
            for i in range(1,len(self.layers)):
                n_layer_weights = self.layers[i] * self.layers[i-1]
                n_layer_biases = self.layers[i]
                weights = individual[offset:(offset+n_layer_weights)].reshape(self.layers[i],self.layers[i-1])
                offset = offset + n_layer_weights
                biases = individual[offset:(offset+n_layer_biases)].reshape(self.layers[i],1)
                offset = offset + n_layer_biases
                activation = np.matmul(weights,activation) + biases
                if i != len(self.layers)-1:
                    #activation = activation * (activation>0)
                    activation = 1.0 / (1.0 + np.exp(-activation))
            assert(offset == len(self.create_individual()))
            decision = np.argmax(activation)
            return ['U','D','L','R'][decision]
            #print(activation.reshape(1, -1))
            if decision == 0:
                return snake.direction
            elif decision == 1:
                if snake.direction == 'U':
                    return 'L'
                elif snake.direction == 'L':
                    return 'D'
                elif snake.direction == 'R':
                    return 'U'
                elif snake.direction == 'D':
                    return 'R'
            elif decision == 2:
                if snake.direction == 'U':
                    return 'R'
                elif snake.direction == 'L':
                    return 'U'
                elif snake.direction == 'R':
                    return 'D'
                elif snake.direction == 'D':
                    return 'L'

        return controller

    def calculate_fitness(self,individual):
        controller = self.convert_individual_to_game_controller(individual)
        game.set_controller(controller)
        fitness = game.play()
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_individual = individual
        return fitness

    def next_generation(self,prev_generation=None,fitness=None):
        if prev_generation is None:
            return np.array([self.create_individual() for _ in range(self.population_size)])
        print('New generation via GA...')

        fitness = fitness - np.min(fitness)
        fitness_normalized = (fitness) / np.sum((fitness))

        #print('fitness normalized: ',fitness_normalized)
        #print(fitness_normalized)

        elites = []
        generation = []
        fitness_normalized_copy = fitness_normalized.copy()
        for _ in range(self.elite_parents):
            index = np.argmax(fitness_normalized)
            elites.append(prev_generation[index])
            generation.append(prev_generation[index])
            fitness_normalized[index] = -1000

        for _ in range(self.population_size-self.elite_parents):
            index1, index2 = np.random.choice(len(fitness_normalized),size=2,replace=False,p=fitness_normalized_copy)
            child = self.mutate(self.cross_over(prev_generation[index1],prev_generation[index2],mode=2))
            generation.append(child)

        return np.array(generation)

    def run(self):
        prev_generation = None
        fitness = None
        self.best_individual = None
        self.best_fitness = 0
        for n in range(self.generations):
            prev_generation = self.next_generation(prev_generation,fitness)
            fitness = np.array([1.0 + self.calculate_fitness(individual) for individual in prev_generation])
            #print('fitness',fitness)
            print("Generation %d\nBest Fitness: %d\n"%(n,np.max(fitness)))
