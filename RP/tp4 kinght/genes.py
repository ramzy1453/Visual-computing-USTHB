import random

# Paramètres de l'algorithme génétique
population_size = 100
mutation_rate = 0.01
target_phrase = "Hello, World!"


# Fonction pour générer une population initiale de chaînes aléatoires
def generate_population(size):
    return [
        "".join(
            random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.!?")
            for _ in range(len(target_phrase))
        )
        for _ in range(size)
    ]


# Fonction pour évaluer la fitness d'une solution par rapport à la phrase cible
def calculate_fitness(solution):
    return sum(1 for s, t in zip(solution, target_phrase) if s == t)


# Fonction pour sélectionner des individus en fonction de leur fitness
def selection(population, scores):
    return random.choices(population, weights=scores, k=len(population))


# Fonction pour effectuer le croisement (crossover) entre deux solutions
def crossover(parent1, parent2):
    split_point = random.randint(0, len(parent1) - 1)
    return parent1[:split_point] + parent2[split_point:]


# Fonction pour appliquer une mutation à une solution
def mutate(solution):
    mutated_solution = list(solution)
    for i in range(len(mutated_solution)):
        if random.random() < mutation_rate:
            mutated_solution[i] = random.choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.!?"
            )
    return "".join(mutated_solution)


# Algorithme génétique principal
def genetic_algorithm():
    population = generate_population(population_size)
    print(population)

    for generation in range(1000):
        # Calcul de la fitness pour chaque individu de la population
        fitness_scores = [calculate_fitness(individual) for individual in population]
        print(generation, fitness_scores)
        # Vérification si la solution optimale est atteinte
        if max(fitness_scores) == len(target_phrase):
            print("Solution trouvée à la génération", generation)
            break

        # Sélection des individus pour la reproduction
        selected_population = selection(population, fitness_scores)
        print(selected_population)
        # Création d'une nouvelle génération en croisant et mutant les individus sélectionnés
        new_population = [
            crossover(
                random.choice(selected_population), random.choice(selected_population)
            )
            for _ in range(population_size)
        ]
        print(new_population)

        new_population = [mutate(individual) for individual in new_population]
        # Remplacement de l'ancienne population par la nouvelle génération
        population = new_population

    # Affichage de la meilleure solution trouvée
    best_solution = max(population, key=calculate_fitness)
    print("Meilleure solution trouvée :", best_solution)

    # Exécution de l'algorithme génétique


# genetic_algorithm()

arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def create_combinaison(arr):
    combinaison = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            combinaison.append((arr[i], arr[j]))
    return combinaison


def fn(x):
    return x**2


def csp(values, domains, constraint):
    return ""
