'''
To help yourself get to and from your bunk every day, write a function called 
solution(src, dest) which takes in two parameters: the source square, on which you start,
 and the destination square, which is where you need to land to solve the puzzle. 
The function should return an integer representing the smallest number of moves it will 
take for you to travel from the source square to the destination square using a chess 
knight's moves (that is, two squares in any direction immediately followed by one square 
perpendicular to that direction, or vice versa, in an "L" shape).  Both the source and destination
squares will be an integer between 0 and 63, inclusive, and are numbered like the example chessboard below:

-------------------------
| 0| 1| 2| 3| 4| 5| 6| 7|
-------------------------
| 8| 9|10|11|12|13|14|15|
-------------------------
|16|17|18|19|20|21|22|23|
-------------------------
|24|25|26|27|28|29|30|31|
-------------------------
|32|33|34|35|36|37|38|39|
-------------------------
|40|41|42|43|44|45|46|47|
-------------------------
|48|49|50|51|52|53|54|55|
-------------------------
|56|57|58|59|60|61|62|63|
-------------------------

-- Python cases -- 
Input:
solution.solution(0, 1)
Output:
    3

Input:
solution.solution(19, 36)
Output:
    1
'''


def is_valid(node):
    if node >= 0 and node <= 63:
        return True
    else:
        return False


def get_adjs(node):
    path_list = []
    possible_endpoints = [
        node + 17 if node % 8 < 7 else -1, node +
        15 if node % 8 != 0 else -1,  # downward
        node + 10 if node % 8 < 6 else -1, node - \
        6 if node % 8 < 6 else -1,  # right
        node - 15 if node % 8 < 7 else -1, node - \
        17 if node % 8 != 0 else -1,  # upward
        node - 10 if node % 8 > 1 else -1, node + 6 if node % 8 > 1 else -1,  # left
    ]
    for point in possible_endpoints:
        if is_valid(point):
            path_list.append(point)
    return path_list


def solution(src, dest):
    if src == dest:
        return 0
    # visited all to -1
    visited = [-1] * 64
    # q for iterate nodes
    queue = []
    # set src to 0
    visited[src] = 0
    queue.append(src)
    while queue:
        curr = queue.pop(0)
        for adj in get_adjs(curr):
            if visited[adj] == -1 or visited[adj] > visited[curr] + 1:
                visited[adj] = visited[curr] + 1
                queue.append(adj)
    # print_mtx(visited)
    return visited[dest]


def print_mtx(visited):
    for x in [visited[x:y] for x, y in [(0, 8), (8, 16), (16, 24), (24, 32)]]:
        print(*x)
    print()


print(solution(19, 36))
