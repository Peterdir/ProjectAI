import time
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal, callback=None, update_callback=None):
    ROWS, COLS = len(maze), len(maze[0])
    open_list = []
    heapq.heappush(open_list, (heuristic(start, goal), start, [start]))
    visited = set()

    stats = {"Steps": 0, "Visited nodes": 0, "Path length": 0, "Time (ms)": 0.0}
    t0 = time.time()

    while open_list:
        _, (x, y), path = heapq.heappop(open_list)
        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if (x, y) == goal:
            return path, stats

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
                heapq.heappush(open_list, (heuristic((nx, ny), goal), (nx, ny), path + [(nx, ny)]))
                if callback:
                    callback((nx, ny))

    stats["Visited nodes"] = len(visited)
    stats["Time (ms)"] = (time.time() - t0) * 1000
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))
    return None, stats
