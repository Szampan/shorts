from icecream import ic

n = 10
masses = [3015, 4728, 4802, 4361, 135, 4444, 4313, 1413, 4581, 546]
initial_order = [3, 10, 1, 8, 9, 4, 2, 7, 6, 5]
target_order = [4, 9, 5, 3, 1, 6, 10, 7, 8, 2]
# n = 6
# masses = [2400, 2000, 1200, 2400, 1600, 4000]
# initial_order = [1,4,5,3,6,2]
# target_order = [5,3,2,4,6,1]

# shift_graph = {}                         
# for elephant in initial_order:
#     shift_graph[elephant] = initial_order[target_order.index(elephant)]

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
        # print(visited)
        # print()
ic(cycles)

min_mass_global = 6500
total_masses_per_cycle = []
min_masses_per_cycle = []
for cycle in cycles:
    print(f"\nCykl: {cycle}: {cycles[cycle]}")
    total_masses_in_cycle = 0
    min_mass_in_cycle = 6500
    for elephant in cycles[cycle]:
        # print(f"e (słoń): {elephant}")
        # print(f"masa słonia: {get_mass(elephant)}")
        total_masses_in_cycle += get_mass(elephant)    
        min_mass_in_cycle = min(min_mass_in_cycle, get_mass(elephant))
        # print(f"min_cyklu: {min_mass_in_cycle}")
    total_masses_per_cycle.append(total_masses_in_cycle)
    min_masses_per_cycle.append(min_mass_in_cycle)
    min_mass_global = min(min_mass_global, min_mass_in_cycle)
    # print(f"min_ogol: {min_mass_global}")
    
ic(total_masses_per_cycle)

result = 0
print()
ic(cycles)
for i in range(cycle_number):
    # ic(i)
    # ic(total_masses_per_cycle[i])
    # ic(len(cycles[i+1]))
    # ic(min_masses_per_cycle[i])
    method_1 = total_masses_per_cycle[i] + (len(cycles[i+1]) - 2) * min_masses_per_cycle[i]
    method_2 = total_masses_per_cycle[i] + min_masses_per_cycle[i] + (len(cycles[i+1]) + 1) * min_mass_global
    # ic(method_1)
    # ic(method_2)
    result += min(method_1, method_2)

ic(result)
print(result)