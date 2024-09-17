import pulp

# Constants
NUM_PEOPLE = 24
GROUP_SIZE = 6
NUM_DAYS = 6
NUM_GROUPS = NUM_PEOPLE // GROUP_SIZE
REPEATS_ALLOWED = 2

# Create the ILP problem
prob = pulp.LpProblem("Boat_Group_Assignment", pulp.LpMinimize)

# Binary decision variables: x[d][g][p] = 1 if person p is in group g on day d
x = pulp.LpVariable.dicts("x", (range(NUM_DAYS), range(NUM_GROUPS), range(1, NUM_PEOPLE + 1)), 0, 1, pulp.LpBinary)

# Auxiliary binary variables: y[d][p1][p2] = 1 if p1 and p2 are in the same group on day d
y = pulp.LpVariable.dicts("y", (range(NUM_DAYS), range(1, NUM_PEOPLE), range(2, NUM_PEOPLE + 1)), 0, 1, pulp.LpBinary)

# Constraint 1: Each person must be assigned to one group per day
for d in range(NUM_DAYS):
    for p in range(1, NUM_PEOPLE + 1):
        prob += pulp.lpSum(x[d][g][p] for g in range(NUM_GROUPS)) == 1

# Constraint 2: Each group must have exactly 6 people per day
for d in range(NUM_DAYS):
    for g in range(NUM_GROUPS):
        prob += pulp.lpSum(x[d][g][p] for p in range(1, NUM_PEOPLE + 1)) == GROUP_SIZE

# Constraint 3: Define y[d][p1][p2] to be 1 if p1 and p2 are in the same group on day d
for d in range(NUM_DAYS):
    for p1 in range(1, NUM_PEOPLE):
        for p2 in range(p1 + 1, NUM_PEOPLE + 1):
            for g in range(NUM_GROUPS):
                # If both p1 and p2 are in group g on day d, y[d][p1][p2] must be 1
                prob += y[d][p1][p2] >= x[d][g][p1] + x[d][g][p2] - 1

# Constraint 4: No pair of people can be in the same group more than REPEATS_ALLOWED times
for p1 in range(1, NUM_PEOPLE):
    for p2 in range(p1 + 1, NUM_PEOPLE + 1):
        prob += pulp.lpSum(y[d][p1][p2] for d in range(NUM_DAYS)) <= REPEATS_ALLOWED

# Solve the ILP problem
prob.solve(pulp.PULP_CBC_CMD(msg=True))  # Enable verbose solver output

# Output the solution
if prob.status == pulp.LpStatusOptimal:
    for d in range(NUM_DAYS):
        print(f"Day {d + 1}:")
        for g in range(NUM_GROUPS):
            group = [p for p in range(1, NUM_PEOPLE + 1) if pulp.value(x[d][g][p]) == 1]
            print(group)
        print()
        print()
else:
    print("No optimal solution found.")
