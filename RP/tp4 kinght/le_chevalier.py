import pygame
from random import random, randint

width, height = 600, 600
square_size = width // 8

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chevalier")
clock = pygame.time.Clock()


class Chevalier:
    moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    def __init__(self, genetic=None):
        self.position = (0, 0)
        self.path = [self.position]
        self.genetic = genetic if genetic is not None else Genetic()
        self.fitness = 0

    def move_forward(self, direction):
        x, y = self.position
        dx, dy = Chevalier.moves[direction]
        new_position = (x + dx, y + dy)
        if (
            new_position[0] > -1
            and new_position[0] < 8
            and new_position[1] > -1
            and new_position[1] < 8
            and (new_position not in self.path)
        ):
            self.path.append(new_position)
            self.position = new_position
            return True
        return False

    def move_backward(self, direction, i):
        new_move = 0
        for x in range(1, 7):
            new_move = (direction + x) % 8
            if self.move_forward(new_move):
                self.genetic.genes[i] = new_move
                return True
        return False

    def check_moves(self):
        for x in range(63):
            if not self.move_forward(self.genetic.genes[x]):
                if not self.move_backward(self.genetic.genes[x], x):
                    break

    def evaluate_fitness(self):
        self.fitness = len(self.path)
        return self.fitness


class Genetic:
    mutation_rate = 0.01

    def __init__(self, genes=None):
        self.genes = genes if genes is not None else self.random_genes()

    def random_genes(self):
        genes = []
        for _ in range(64):
            genes.append(randint(0, 7))
        print(genes[0])
        return genes

    def cross_over(self, parent):
        child1 = self.genes[0:32] + parent.genes[32:63]
        child2 = self.genes[32:63] + parent.genes[0:32]
        return Genetic(child1), Genetic(child2)

    def mutate(self):
        for i in range(63):
            mutation_proba = random()
            if mutation_proba < Genetic.mutation_rate:
                self.genes[i] = randint(0, 7)


class Population:
    def __init__(self, population_size, generation=1):
        self.population_size = population_size
        self.generation = generation
        self.chevaliers = [Chevalier() for _ in range(self.population_size)]

    def check_population(self):
        for chevalier in self.chevaliers:
            chevalier.check_moves()

    def evaluate(self):
        best_chevalier = None
        max_fit = 0
        for chevalier in self.chevaliers:
            fit = chevalier.evaluate_fitness()
            if fit > max_fit:
                max_fit = fit
                best_chevalier = chevalier
        return max_fit, best_chevalier

    def tournament_selection(self, size):
        tournament = []
        for i in range(size):
            X = randint(0, self.population_size - 1)
            tournament.append(self.chevaliers[X])
        parent1 = None
        parent2 = None
        for chevalier in tournament:
            if parent1 is None or parent1.fitness < chevalier.fitness:
                parent2 = parent1
                parent1 = chevalier
            elif parent2 is None or parent2.fitness < chevalier.fitness:
                parent2 = chevalier

        return parent1, parent2

    def create_new_generation(self):
        new_population = []
        tournament_size = 10
        for _ in range(self.population_size // 2):
            parent1, parent2 = self.tournament_selection(tournament_size)
            child1, child2 = parent1.genetic.cross_over(parent2.genetic)
            child1.mutate()
            child2.mutate()
            new_population.append(Chevalier(child1))
            new_population.append(Chevalier(child2))
        for chevalier in new_population:
            chevalier.genetic.mutate()
        self.chevaliers = new_population


def convert_coordinates(position):
    x, y = position
    return y * square_size, x * square_size


def draw_board():
    for row in range(8):
        for col in range(8):
            color = (255, 255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0, 255)
            pygame.draw.rect(
                screen,
                color,
                (col * square_size, row * square_size, square_size, square_size),
            )


def draw_chevalier(position):
    x, y = convert_coordinates(position)
    knight_image = pygame.image.load("chevalier.png")
    knight_image = pygame.transform.scale(knight_image, (square_size, square_size))
    knight_rect = knight_image.get_rect(
        center=(x + square_size // 2, y + square_size // 2)
    )
    screen.blit(knight_image, knight_rect)


population_size = 50
population = Population(population_size)
num_gen = 0
running = True
step = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    population.check_population()
    max_fit, best_chevalier = population.evaluate()

    if max_fit == 64:
        screen.fill((0, 0, 0, 255))
        draw_board()

        if best_chevalier is not None:
            font = pygame.font.Font(None, 20)
            text = font.render(f"{step}", True, (0, 0, 0))
            for position in best_chevalier.path:
                if best_chevalier.position != position:
                    x, y = convert_coordinates(position)
                    text = pygame.font.Font(None, 36).render(str(step), True, (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(x + square_size // 2, y + square_size // 2)
                    )
                    draw_chevalier(position)
                    screen.blit(text, text_rect)
                    step += 1
                    transparent_surface = pygame.Surface(
                        (square_size, square_size), pygame.SRCALPHA
                    )
                    screen.blit(transparent_surface, (x, y))
                    pygame.display.update()
                    clock.tick(2)
                    draw_board()
        break

    num_gen += 1
    population.create_new_generation()

pygame.quit()
