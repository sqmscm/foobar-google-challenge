'''
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and broken the bunnies out of Lambda's prison
 - and now you need to escape from the space station as quickly and as orderly as possible!
  The bunnies have all gathered in various locations throughout the station, and need to 
  make their way towards the seemingly endless amount of escape pods positioned in other 
  parts of the station. You need to get the numerous bunnies through the various rooms to 
  the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies 
  at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so 
  they vary in how many bunnies can move through them at a time. 

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods,
and how many bunnies can fit through at a time in each direction of every corridor in between,
figure out how many bunnies can safely make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of integers denoting where
the groups of gathered bunnies are, an array of integers denoting where the escape pods are located,
and an array of an array of integers of the corridors, returning the total number of bunnies that 
can get through at each time step as an int. The entrances and exits are disjoint and thus will never
overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies
at each time step. There are at most 50 rooms connected by the corridors and at most 2000000 bunnies
that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
[0, 0, 4, 6, 0, 0], # Room 0: Bunnies
[0, 0, 5, 2, 0, 0], # Room 1: Bunnies
[0, 0, 0, 0, 4, 4], # Room 2: Intermediate room
[0, 0, 0, 0, 6, 6], # Room 3: Intermediate room
[0, 0, 0, 0, 0, 0], # Room 4: Escape pods
[0, 0, 0, 0, 0, 0], # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.
(Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5,
such as 2/6 and 6/6, but the final solution remains the same.)


-- Python cases -- 
Input:
solution.solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
Output:
    6

Input:
solution.solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], 
[0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    16

'''


class Graph:
    # Use Ford-Fulkerson Algorithm

    def __init__(self, entrances, exits, path):
        self.adj_list = {}
        self.capacity = path
        # add edges to source s and entrances
        self.adj_list['s'] = entrances
        self.solution = 0
        # build a graph from the path
        for node in range(len(path)):
            self.adj_list[node] = []
            for target in range(len(path[node])):
                if path[node][target] > 0:
                    self.adj_list[node].append(target)
        # add edges to sink t and exits
        for e in exits:
            self.adj_list[e].append('t')

    def get_min_capacity(self, path):
        curr = path[0]
        min_capacity = 2000000
        for x in range(1, len(path)):
            curr_cap = self.capacity[curr][path[x]]
            min_capacity = min(min_capacity, curr_cap)
            curr = path[x]
        return min_capacity

    def get_capacity(self, a, b):
        if a == 's' or b == 't':
            return 2000000
        else:
            return self.capacity[a][b]

    def decrease_capacity_on_path(self, path, dec):
        curr = path[0]
        for x in range(1, len(path)):
            self.capacity[curr][path[x]] -= dec
            # self.capacity[path[x]][curr] += dec
            curr = path[x]

    def find_all_paths(self, u, v, visited, path):
        # dfs
        if u != 's':
            visited[u] = True
            path.append(u)
        for node in self.adj_list[u]:
            if node == v:
                # STEP 2: Get the minimum capacity value on the path
                min_cap = self.get_min_capacity(path)
                # STEP 3: Add minimum capacity to total
                self.solution += min_cap
                # STEP 4: Decrease each edge in path by min_cap
                self.decrease_capacity_on_path(path, min_cap)
                # if min_cap > 0:
                #     print(f'{path} {min_cap} {self.solution}')
            elif visited[node] is False and self.get_capacity(u, node) > 0:
                self.find_all_paths(node, v, visited, path)
        if u != 's':
            visited[u] = False
            path.pop()

    def get_solution(self):
        # STEP 1: DFS to find path from s to t
        visited = [False]*len(self.capacity)
        path = []
        self.find_all_paths('s', 't', visited, path)
        return self.solution


def solution(entrances, exits, path):
    graph = Graph(entrances, exits, path)
    return graph.get_solution()


print(solution([0], [3], [[0, 7, 0, 0], [
      0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))
print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [
      0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
