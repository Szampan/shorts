import sys

MAX_MASS = 6500
input_data = [list(map(int, i.split())) for i in sys.stdin]
n, masses, initial_order, target_order = input_data
n = n[0]
shift_graph = [initial_order[target_order.index(i+1)]-1 for i in range(n)]
cycles = [] 
visited = [False] * n
cycle_number = 0  

for i in range(n):
    elephant = i
    if not visited[i]:
        cycles.append(set())
        while not visited[elephant]:
            cycles[cycle_number].add(elephant+1)
            visited[elephant] = True
            elephant = shift_graph[elephant]
        cycle_number += 1

min_mass_global = MAX_MASS
total_masses_per_cycle = []
min_masses_per_cycle = []

for cycle in range(cycle_number):
    total_masses_in_cycle = 0
    min_mass_in_cycle = MAX_MASS

    for elephant in cycles[cycle]:
        total_masses_in_cycle += masses[elephant-1]    
        min_mass_in_cycle = min(min_mass_in_cycle, masses[elephant-1])

    total_masses_per_cycle.append(total_masses_in_cycle)
    min_masses_per_cycle.append(min_mass_in_cycle)
    min_mass_global = min(min_mass_global, min_mass_in_cycle)

result = 0
for i in range(cycle_number):
    method_1 = total_masses_per_cycle[i] + (len(cycles[i]) - 2) * min_masses_per_cycle[i]          
    method_2 = total_masses_per_cycle[i] + min_masses_per_cycle[i] + (len(cycles[i]) + 1) * min_mass_global
    result += min(method_1, method_2)

print(result)