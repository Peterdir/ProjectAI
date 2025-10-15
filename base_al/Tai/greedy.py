import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def cothediduoc(x, y, maze):
    ROWS, COLS = len(maze), len(maze[0])
    result = []
    dirs = [(-1,0),(0,-1),(1,0),(0,1)]  # lên, trái, xuống, phải
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
            result.append((nx, ny))
    return result

def find_path(maze, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), [start]))
    visited = set()

    while open_list:
        _, path = heapq.heappop(open_list)
        current = path[-1]

        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)

        for next_cell in cothediduoc(*current, maze):
            if next_cell not in visited:
                new_path = path + [next_cell]
                heapq.heappush(open_list, (heuristic(next_cell, goal), new_path))
    return None

