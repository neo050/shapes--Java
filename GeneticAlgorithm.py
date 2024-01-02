import random

class Solution:
    def __init__(self, pallet_size, shapes):
        self.pallet_size = pallet_size
        self.shapes = shapes
        self.placement = []  # Store shape placements: (x, y, shape, rotation)
        self.grid = [[False] * pallet_size[1] for _ in range(pallet_size[0])]

    def is_valid_placement(self, shape, x, y, rotated):
        shape_width, shape_height = (shape[1], shape[0]) if rotated else shape
        if x + shape_width > self.pallet_size[0] or y + shape_height > self.pallet_size[1]:
            return False
        for i in range(x, x + shape_width):
            for j in range(y, y + shape_height):
                if self.grid[i][j]:
                    return False
        return True

    def place_shape(self, shape, x, y, rotated):
        shape_width, shape_height = (shape[1], shape[0]) if rotated else shape
        for i in range(x, x + shape_width):
            for j in range(y, y + shape_height):
                self.grid[i][j] = True
        self.placement.append((x, y, shape, rotated))

    def random_placement(self):
        for shape in self.shapes:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(0, self.pallet_size[0] - 1)
                y = random.randint(0, self.pallet_size[1] - 1)
                rotated = random.choice([True, False])
                if self.is_valid_placement(shape, x, y, rotated):
                    self.place_shape(shape, x, y, rotated)
                    placed = True
                attempts += 1


    def adjust_placement(self):
        for i, (x, y, shape, rotated) in enumerate(self.placement):
            if not self.is_valid_placement(shape, x, y, rotated):
                # Attempt to find a new valid position for the shape
                placed = False
                attempts = 0
                while not placed and attempts < 100:
                    x = random.randint(0, self.pallet_size[0] - 1)
                    y = random.randint(0, self.pallet_size[1] - 1)
                    if self.is_valid_placement(shape, x, y, rotated):
                        self.placement[i] = (x, y, shape, rotated)
                        self.update_grid_with_shape(shape, x, y, rotated)
                        placed = True
                    attempts += 1

    def update_grid_with_shape(self, shape, x, y, rotated):
        # Clear the grid and reapply all shapes
        self.grid = [[False] * self.pallet_size[1] for _ in range(self.pallet_size[0])]
        for px, py, pshape, protated in self.placement:
            self.place_shape(pshape, px, py, protated)


class GeneticAlgorithm:
    def __init__(self, population_size, num_generations, pallet_size, shapes):
        self.population_size = population_size
        self.num_generations = num_generations
        self.pallet_size = pallet_size
        self.shapes = shapes
        self.population = []

    def initialize_population(self):
        self.population = []
        for _ in range(self.population_size):
            solution = Solution(self.pallet_size, self.shapes)
            solution.random_placement()
            self.population.append(solution)

    def calculate_fitness(self, individual):
        pallet_area = self.pallet_size[0] * self.pallet_size[1]
        used_area = 0
        overlap_penalty = 0
        grid = [[False] * self.pallet_size[1] for _ in range(self.pallet_size[0])]

        for placement in individual.placement:
            x, y, shape, rotated = placement
            shape_width, shape_height = (shape[1], shape[0]) if rotated else shape
            for i in range(x, min(x + shape_width, self.pallet_size[0])):
                for j in range(y, min(y + shape_height, self.pallet_size[1])):
                    if grid[i][j]:  # Overlap detected
                        overlap_penalty += 1
                    else:
                        grid[i][j] = True
                        used_area += 1
        fitness = used_area - overlap_penalty
        return fitness

    def select_parents(self):
        tournament_size = 5  # You can adjust this size
        parents = []

        for _ in range(2):  # Selecting two parents
            tournament = random.sample(self.population, tournament_size)
            best = max(tournament, key=lambda ind: self.calculate_fitness(ind))
            parents.append(best)

        return parents[0], parents[1]

    def crossover(self, parent1, parent2):
        # Create a deep copy of parent1 to be the base of the offspring
        offspring = Solution(self.pallet_size, self.shapes)
        offspring.placement = parent1.placement.copy()

        # Determine the crossover point
        crossover_point = random.randint(1, len(parent2.placement) - 1)

        # Combine the placements from both parents
        offspring.placement[crossover_point:] = parent2.placement[crossover_point:]

        offspring.adjust_placement()  # Re-validate and adjust the offspring


        return offspring

    def mutate(self, individual):
        # Implement mutation logic
        pass

    def run(self):
        self.initialize_population()
        for generation in range(self.num_generations):
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                offspring = self.crossover(parent1, parent2)
                offspring = self.mutate(offspring)
                new_population.append(offspring)
            self.population = new_population
            # Evaluate fitness and select new generation

if __name__ == "__main__":
    pallet_size = (100, 100)
    shapes = [(10, 20), (15, 15), (5, 5)]  # Define your shapes here

    ga = GeneticAlgorithm(population_size=50, num_generations=100, pallet_size=pallet_size, shapes=shapes)
    ga.run()
