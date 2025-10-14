import time
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal):
    ROWS, COLS = len(maze), len(maze[0])
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start, [start]))
    visited = set()

    while open_list:
        _, (x, y), path = heapq.heappop(open_list)
    
        if (x, y) == goal:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
                heapq.heappush(open_list, (heuristic((nx, ny), goal), (nx, ny), path + [(nx, ny)]))
    return None

# ----- TEST -----
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0]
]

start = (0, 0)
goal = (3, 4)

result = find_path(maze, start, goal)
print(result)
