import sys
from icecream import ic
input_data = [list(map(int, i.split())) for i in sys.stdin]
n, masses, initial_order, target_order = input_data
n = n[0]

shift_graph = {elephant: initial_order[target_order.index(elephant)] for elephant in initial_order}
ic(shift_graph)
cycles = {} 
visited = [False] * n
cycle_number = 0   

def mark_vertex_visited(elephant):
    if not visited[elephant-1]:
        visited[elephant-1] = True
        cycles[cycle_number].append(elephant)
        mark_vertex_visited(shift_graph[elephant])

def get_mass(elephant):
    return masses[elephant-1]

for i in range(n):
    elephant = i + 1 
    if not visited[i]:
        cycle_number += 1
        cycles[cycle_number] = []
        mark_vertex_visited(elephant)

min_mass_global = 6500
total_masses_per_cycle = []
min_masses_per_cycle = []

for cycle in cycles:
    total_masses_in_cycle = 0
    min_mass_in_cycle = 6500

    for elephant in cycles[cycle]:
        total_masses_in_cycle += get_mass(elephant)    
        min_mass_in_cycle = min(min_mass_in_cycle, get_mass(elephant))

    total_masses_per_cycle.append(total_masses_in_cycle)
    min_masses_per_cycle.append(min_mass_in_cycle)
    min_mass_global = min(min_mass_global, min_mass_in_cycle)

result = 0
for i in range(cycle_number):
    method_1 = total_masses_per_cycle[i] + (len(cycles[i+1]) - 2) * min_masses_per_cycle[i]
    method_2 = total_masses_per_cycle[i] + min_masses_per_cycle[i] + (len(cycles[i+1]) + 1) * min_mass_global
    result += min(method_1, method_2)

print(result)

