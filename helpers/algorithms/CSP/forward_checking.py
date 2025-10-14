import time

def get_neighbors(pos, maze, visited):
    ROWS, COLS = len(maze), len(maze[0])
    x, y = pos
    neighbors = []
    for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
            neighbors.append((nx, ny))
    return neighbors

def forward_check(pos, maze, visited, goal):
    """Kiểm tra trước xem từ pos có neighbor khả thi nào không (hoặc chính là goal)."""
    if pos == goal:
        return True
    return len(get_neighbors(pos, maze, visited)) > 0

def backtrack(maze, current, goal, visited, path, stats, t0, callback, update_callback):
    stats["Steps"] += 1
    stats["Visited nodes"] = len(visited)
    stats["Path length"] = len(path)
    stats["Time (ms)"] = (time.time() - t0) * 1000

    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))

    if current == goal:
        return path

    for nx, ny in get_neighbors(current, maze, visited):
        if forward_check((nx, ny), maze, visited, goal):
            visited.add((nx, ny))
            path.append((nx, ny))
            if callback:
                callback((nx, ny))

            result = backtrack(maze, (nx, ny), goal, visited, path, stats, t0, callback, update_callback)
            if result:
                return result

            # nếu thất bại thì quay lui
            path.pop()
            visited.remove((nx, ny))
    return None

def find_path(maze, start, goal, callback=None, update_callback=None):
    visited = set([start])
    path = [start]

    stats = {"Steps": 0, "Visited nodes": 0, "Path length": 0, "Time (ms)": 0.0}
    t0 = time.time()

    result = backtrack(maze, start, goal, visited, path, stats, t0, callback, update_callback)

    stats["Visited nodes"] = len(visited)
    stats["Time (ms)"] = (time.time() - t0) * 1000
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))

    if result:
        return result, stats
    return None, stats
