import numpy as np
from scipy.optimize import linprog

print("--- Initializing Supply Chain Optimization Engine ---\n")

# Network Parameters
# Factories: Chicago, Dallas
supply_capacities = [500, 700] 

# Warehouses: New York, Atlanta, Los Angeles
demand_requirements = [400, 400, 300]

# Cost Matrix (Rows = Factories, Columns = Warehouses)
cost_matrix = [
    [2, 4, 7],  # Chicago to [NY, ATL, LA]
    [5, 3, 4]   # Dallas to [NY, ATL, LA]
]

# Flatten the cost matrix into a 1D vector for the solver
c = np.array(cost_matrix).flatten()

# Setup Inequality Constraints (Supply cannot exceed capacities)
# x0+x1+x2 <= 500 (Chicago Supply)
# x3+x4+x5 <= 700 (Dallas Supply)
A_ub = [
    [1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1]
]
b_ub = supply_capacities

# Setup Equality Constraints (Demand must match requirements exactly)
# x0 + x3 = 400 (New York Demand)
# x1 + x4 = 400 (Atlanta Demand)
# x2 + x5 = 300 (Los Angeles Demand)
A_eq = [
    [1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1]
]
b_eq = demand_requirements

# Run the Optimization Bounds 
bounds = [(0, None) for _ in range(len(c))]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Display the Operational Output
if res.success:
    optimal_routes = res.x.reshape(2, 3)
    print(f"Optimization Successful. Minimum Logistics Cost: ${res.fun:,.2f}\n")
    
    factories = ["Chicago", "Dallas"]
    warehouses = ["New York", "Atlanta", "Los Angeles"]
    
    for i, factory in enumerate(factories):
        for j, warehouse in enumerate(warehouses):
            units = optimal_routes[i][j]
            if units > 0:
                print(f" Route: Route {units:>4.0f} units from {factory:<8} -> {warehouse:<12} at ${cost_matrix[i][j]}/unit")
else:
    print("Optimization failed. Check supply/demand balances.")
