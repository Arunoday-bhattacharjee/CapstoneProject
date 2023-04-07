import random

# Define the parameters of the problem
num_sellers = 5
num_buyers = 5
total_supply = 40
total_demand = 40
seller_prices = [1, 2, 3, 4, 5]
seller_supplies = [2, 3, 5, 10, 20]
buyer_prices = [10, 9, 8, 7, 6]
buyer_demands = [7, 8, 4, 10, 11]

# Define the genetic algorithm parameters
pop_size = 50
num_generations = 100
mutation_rate = 0.05

# Define the fitness function
def calculate_fitness(individual):
    seller_mask = individual[:num_sellers]
    buyer_mask = individual[num_sellers:]
    seller_indices = [i for i in range(num_sellers) if seller_mask[i]]
    buyer_indices = [i for i in range(num_buyers) if buyer_mask[i]]
    seller_supply = sum([seller_supplies[i] for i in seller_indices])
    buyer_demand = sum([buyer_demands[i] for i in buyer_indices])
    if seller_supply < buyer_demand:
        return 0
    total_profit = 0
    trades = []
    seller_index = 0
    buyer_index = 0
    while seller_index < num_sellers and buyer_index < num_buyers:
        seller_price = seller_prices[seller_indices[seller_index]]
        buyer_price = buyer_prices[buyer_indices[buyer_index]]
        if seller_price < buyer_price:
            seller_index += 1
        elif seller_price > buyer_price:
            buyer_index += 1
        else:
            trade_quantity = min(seller_supplies[seller_indices[seller_index]], buyer_demands[buyer_indices[buyer_index]])
            total_profit += trade_quantity * seller_price
            trades.append((buyer_indices[buyer_index], seller_indices[seller_index], trade_quantity))
            seller_supplies[seller_indices[seller_index]] -= trade_quantity
            buyer_demands[buyer_indices[buyer_index]] -= trade_quantity
            if seller_supplies[seller_indices[seller_index]] == 0:
                seller_index += 1
            if buyer_demands[buyer_indices[buyer_index]] == 0:
                buyer_index += 1
    return total_profit

# Define the genetic algorithm functions
def generate_population(pop_size):
    population = []
    for i in range(pop_size):
        individual = [random.randint(0, 1) for _ in range(num_sellers + num_buyers)]
        population.append(individual)
    return population

def crossover(parent1, parent2):
    crossover_point = random.randint(0, num_sellers + num_buyers - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate):
    for i in range(num_sellers + num_buyers):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

# Generate the initial population
population = generate_population(pop_size)

# Run the genetic algorithm
for generation in range(num_generations):
    # Evaluate the fitness of each individual in the population
    fitness_values = [calculate_fitness(individual) for individual in population]
    max_fitness = max(fitness_values)
    max_fitness_index = fitness_values.index(max_fitness)
    best_individual = population[max_fitness_index]
    total_profit = max_fitness

    # Print the progress
    print(f"Generation {generation+1}: Total Profit = {total_profit}")

    # Perform selection, crossover and mutation to generate the next generation
    new_population = []
    for i in range(pop_size):
        # Selection
        parent1_index = random.randint(0, pop_size-1)
        parent2_index = random.randint(0, pop_size-1)
        while parent2_index == parent1_index:
            parent2_index = random.randint(0, pop_size-1)
        parent1 = population[parent1_index]
        parent2 = population[parent2_index]

        # Crossover
        child1, child2 = crossover(parent1, parent2)

        # Mutation
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)

        # Add the children to the new population
        new_population.append(child1)
        new_population.append(child2)

    # Replace the old population with the new population
    population = new_population

# Print the trades made in the best solution found
seller_indices = [i for i in range(num_sellers) if best_individual[i]]
buyer_indices = [i for i in range(num_buyers) if best_individual[num_sellers+i]]
seller_supply = sum([seller_supplies[i] for i in seller_indices])
buyer_demand = sum([buyer_demands[i] for i in buyer_indices])
trades = []
seller_index = 0
buyer_index = 0
while seller_index < num_sellers and buyer_index < num_buyers:
    seller_price = seller_prices[seller_indices[seller_index]]
    buyer_price = buyer_prices[buyer_indices[buyer_index]]
    if seller_price < buyer_price:
        seller_index += 1
    elif seller_price > buyer_price:
        buyer_index += 1
    else:
        trade_quantity = min(seller_supplies[seller_indices[seller_index]], buyer_demands[buyer_indices[buyer_index]])
        trades.append((buyer_indices[buyer_index], seller_indices[seller_index], trade_quantity))
        seller_supplies[seller_indices[seller_index]] -= trade_quantity
        buyer_demands[buyer_indices[buyer_index]] -= trade_quantity
        if seller_supplies[seller_indices[seller_index]] == 0:
            seller_index += 1
        if buyer_demands[buyer_indices[buyer_index]] == 0:
            buyer_index += 1

# Print the results
print(f"\nBest Solution Found: Total Profit = {total_profit}")
print("Trades Made:")
for trade in trades:
    buyer_index, seller_index, quantity = trade
    buyer_id = f"Buyer {buyer_index+1}"
    seller_id = f"Seller {seller_index+1}"
    print(f"{quantity} units of energy traded from {seller_id} to {buyer_id}")
