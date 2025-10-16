import heapq
import time

# Hàm đếm số lượng tường xung quanh ô (x, y)
def count_walls(maze, x, y):
    rows, cols = len(maze), len(maze[0])
    walls = 0

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),       # 4 hướng thẳng
        (-1, -1), (-1, 1), (1, -1), (1, 1)      # 4 hướng chéo
    ]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= rows or ny < 0 or ny >= cols or maze[nx][ny] == 1:
            walls += 1

    return walls


def find_path(maze, start, goal, callback=None, update_callback=None):
    rows, cols = len(maze), len(maze[0])
    frontier = [(0, start, [start])]  # (cost, node, path)
    visited = set()
    steps = 0
    t0 = time.time()
    stats = {}

    while frontier:
        cost, (x, y), path = heapq.heappop(frontier)
        steps += 1

        stats = {
            "Steps": steps,
            "Visited nodes": len(visited),
            "Current node": (x, y),
            "Frontier size": len(frontier),
            "Path length": len(path),
            "Cost": cost,
            "Time (ms)": (time.time() - t0) * 1000
        }

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if (x, y) == goal:
            return path, stats

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if callback:
            callback((x, y))

        # Duyệt các ô kề (ưu tiên ô ít tường)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                wall_penalty = count_walls(maze, nx, ny)
                
                # Nếu bị tường bao quanh 8 hướng thì bỏ qua
                if wall_penalty == 8:
                    continue

                new_cost = cost + 1 + wall_penalty
                heapq.heappush(frontier, (new_cost, (nx, ny), path + [(nx, ny)]))

    return None, stats
