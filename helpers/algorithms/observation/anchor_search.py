import time
from collections import deque

def heuristic_to_anchor(vitri, neo):
    """Dùng Manhattan đến neo"""
    x, y = vitri
    ax, ay = neo
    return abs(x - ax) + abs(y - ay)

def find_path(maze, start, goal, neo=(2,2), callback=None, update_callback=None):
    ROWS = len(maze)
    COLS = len(maze[0])
    visited = set()
    queue = deque([(start, [start], False)])  # (vị trí, đường đi, đã qua neo chưa?)

    stats = {
        "Steps": 0,
        "Visited nodes": 0,
        "Path length": 0,
        "Time (ms)": 0.0
    }
    t0 = time.time()

    while queue:
        (x, y), path, check_neo = queue.popleft()
        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        # Nếu đã đến goal và đã qua neo là thành công
        if (x, y) == goal and check_neo:
            return path, stats

        
        if (x, y, check_neo) in visited:
            continue
        visited.add((x, y, check_neo)) 

        # Loại trường hợp cách xa neo
        if not check_neo:
            if heuristic_to_anchor((x, y), neo) > 20:
                continue

        # Sinh các trạng thái mới (BFS)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                new_passed = check_neo or (nx, ny) == neo
                queue.append(((nx, ny), path + [(nx, ny)], new_passed))  #  path + [(nx, ny)]
                if callback:
                    callback((nx, ny))

    # Không tìm thấy
    stats["Visited nodes"] = len(visited)
    stats["Time (ms)"] = (time.time() - t0) * 1000
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))
    return None, stats
