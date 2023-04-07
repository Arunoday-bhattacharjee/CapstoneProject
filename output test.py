import random

# Generate a random number between 100 and 1000
total_energy = random.randint(100, 1000)

# Divide the total energy into smaller parts for seller supplies
num_sellers = 5
seller_supplies = [random.randint(1, total_energy) for i in range(num_sellers)]
seller_prices = [random.randint(10, 50) for i in range(num_sellers)]
sellers = [('Seller'+str(i), seller_supplies[i], seller_prices[i]) for i in range(num_sellers)]

# Divide the total energy into smaller parts for buyer demands
num_buyers = 5
buyer_demands = [random.randint(1, total_energy) for i in range(num_buyers)]
buyer_prices = [random.randint(10, 50) for i in range(num_buyers)]
buyers = [('Buyer'+str(i), buyer_demands[i], buyer_prices[i]) for i in range(num_buyers)]

# Check that total supply equals total demand
total_supply = sum(seller_supplies)
total_demand = sum(buyer_demands)
if total_supply != total_demand:
    diff = abs(total_supply - total_demand)
    # If total supply > total demand, decrease a random seller's supply by diff
    if total_supply > total_demand:
        seller_index = random.randint(0, num_sellers-1)
        sellers[seller_index] = (sellers[seller_index][0], sellers[seller_index][1]-diff, sellers[seller_index][2])
        total_supply -= diff
    # If total demand > total supply, increase a random buyer's demand by diff
    else:
        buyer_index = random.randint(0, num_buyers-1)
        buyers[buyer_index] = (buyers[buyer_index][0], buyers[buyer_index][1]+diff, buyers[buyer_index][2])
        total_demand -= diff

print("Sellers:", sellers)
print("Buyers:", buyers)
print("Total supply:", total_supply)
print("Total demand:", total_demand)
