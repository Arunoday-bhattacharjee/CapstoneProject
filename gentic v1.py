import random
NUM_SELLERS = 7
NUM_BUYERS = 10
DEMAND = 100
SUPPLY = 100
MIN_PRICE = 1
MAX_PRICE = 10
# Define the chromosome representation
def create_chromosome():
    global NUM_SELLERS, NUM_BUYERS, DEMAND, SUPPLY, MIN_PRICE, MAX_PRICE
    chromosome = {}
    # Initialize demand and supply for this chromosome
    chromosome_demand = random.randint(0, DEMAND)
    chromosome_supply = random.randint(0, SUPPLY)
    for i in range(NUM_SELLERS):
        seller_price = random.randint(MIN_PRICE, MAX_PRICE)
        seller_supply = min(chromosome_supply, SUPPLY)
        for j in range(NUM_BUYERS):
            buyer_price = random.randint(MIN_PRICE, MAX_PRICE)
            if buyer_price >= seller_price:
                quantity = min(seller_supply, max(0, chromosome_demand - DEMAND))
                chromosome[(i, j, seller_price)] = quantity
                seller_supply -= quantity
                DEMAND += quantity
                SUPPLY -= quantity
                if seller_supply == 0 or DEMAND == chromosome_demand or SUPPLY == chromosome_supply:
                    break
        if seller_supply == 0 or DEMAND == chromosome_demand or SUPPLY == chromosome_supply:
            break
    return chromosome


def calculate_fitness(chromosome):
    global NUM_SELLERS, NUM_BUYERS, DEMAND, SUPPLY, MIN_PRICE, MAX_PRICE
    total_profit = 0
    for i in range(NUM_SELLERS):
        seller_price = MAX_PRICE
        seller_supply = 0
        for j in range(NUM_BUYERS):
            if chromosome is not None and (i, j, seller_price) in chromosome:
                seller_supply += chromosome[(i, j, seller_price)]
                total_profit += chromosome[(i, j, seller_price)] * (seller_price - (i, j, seller_price)[2])
        if seller_supply > SUPPLY:
            return 0
        SUPPLY -= seller_supply
        if SUPPLY == 0:
            break
    return (total_profit, chromosome)  # return tuple of (fitness_value, chromosome)

# Define the genetic algorithm
POPULATION_SIZE = 50
NUM_GENERATIONS = 100
ELITE_SIZE = 5

def crossover(parent1, parent2):
    global NUM_SELLERS, NUM_BUYERS
    child1 = {}
    child2 = {}
    for i in range(NUM_SELLERS):
        for j in range(NUM_BUYERS):
            seller_price = MAX_PRICE
            if (i, j, seller_price) in parent1 and (i, j, seller_price) in parent2:
                quantity = (parent1[(i, j, seller_price)] + parent2[(i, j, seller_price)]) // 2
                child1[(i, j, seller_price)] = quantity
                child2[(i, j, seller_price)] = quantity
            elif (i, j, seller_price) in parent1:
                child1[(i, j, seller_price)] = parent1[(i, j, seller_price)]
            elif (i, j, seller_price) in parent2:
                child2[(i, j, seller_price)] = parent2[(i, j, seller_price)]
    return child1, child2
def mutation(chromosome):
    global NUM_SELLERS, NUM_BUYERS, DEMAND, SUPPLY, MIN_PRICE, MAX_PRICE
    i = random.randint(0, NUM_SELLERS - 1)
    j = random.randint(0, NUM_BUYERS - 1)
    seller_price = random.randint(MIN_PRICE, MAX_PRICE)
    if (i, j, seller_price) in chromosome:
        quantity = min(SUPPLY, DEMAND) - chromosome[(i, j, seller_price)]
        if quantity > 0:
            chromosome[(i, j, seller_price)] += quantity
            SUPPLY -= quantity
def genetic_algorithm():
    # Initialization
    population = []
    for i in range(POPULATION_SIZE):
        population.append(create_chromosome())
    
    # Main loop
    for generation in range(NUM_GENERATIONS):
        # Evaluate fitness
        fitness_values = [calculate_fitness(chromosome) for chromosome in population]
        best_chromosome = max(fitness_values, key=lambda x: x[0])[1]
        
        # Elitism
        sorted_population = [chromosome for _, chromosome in sorted(fitness_values, key=lambda x: x[0], reverse=True)]
        elite = sorted_population[:ELITE_SIZE]        
        # Crossover
        children = []
        for i in range(POPULATION_SIZE - ELITE_SIZE):
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child1, child2 = crossover(parent1, parent2)
            children.append(child1)
            children.append(child2)
        
        # Mutation
        for i in range(len(children)):
            if random.random() < 0.1:
                children[i] = mutation(children[i])
        
        # Create new population
        population = elite + children
        
    # Evaluate fitness of final population
    fitness_values = [calculate_fitness(chromosome) for chromosome in population]
    best_chromosome = max(fitness_values, key=lambda x: x[0])[1]
    



    trades = [(i, j, best_chromosome[(i, j, seller_price)]) for i in range(NUM_SELLERS) for j in range(NUM_BUYERS) for seller_price in range(MIN_PRICE, MAX_PRICE+1) if (i, j, seller_price) in best_chromosome]


    total_profit = calculate_fitness(best_chromosome)
    print("Trades:", trades)
    
    
    print("Total profit:", total_profit)

genetic_algorithm()

