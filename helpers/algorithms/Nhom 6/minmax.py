import time

def heuristic(vitri, goal):
    x, y = vitri
    gx, gy = goal
    return abs(x - gx) + abs(y - gy)

def minimax_dfs(maze, current, goal, depth, is_maximizing, visited):
    if depth == 0 or current == goal:
        return -heuristic(current, goal), [current]
    
    visited.add(current)
    moves = []
    ROWS = len(maze)
    COLS = len(maze[0])
    x, y = current

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
            moves.append((nx, ny))
    
    if not moves:
        return -heuristic(current, goal), [current]
    
    best_path = []
    
    if is_maximizing:
        best_score = float('-inf')
        for move in moves:
            score, path = minimax_dfs(maze, move, goal, depth - 1, False, visited.copy())
            if score > best_score:
                best_score = score
                best_path = [current] + path
        return best_score, best_path
    
    else:
        best_score = float('inf')
        for move in moves:
            score, path = minimax_dfs(maze, move, goal, depth - 1, True, visited.copy())
            if score < best_score:
                best_score = score
                best_path = [current] + path
        return best_score, best_path

def choose_start_near_goal(maze, goal):
    gx, gy = goal
    candidates = [
        (gx - 2, gy - 2),
        (gx - 1, gy),
        (gx, gy - 1),
        (gx + 1, gy),
        (gx, gy + 1)
    ]
    for x, y in candidates:
        if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0:
            return (x, y)
    return (0, 0)  # fallback

def find_path(maze, start, goal, callback=None, update_callback=None):
    
    start = (12,18)

    stats = {
        "Steps": 0,
        "Visited Nondes": 0,
        "Path length": 0,
        "Time (ms)": 0
    }
    t0 = time.time()

    MAX_DEPTH = 80
    score, path = minimax_dfs(maze, start, goal, MAX_DEPTH, True, set())

    visited_nodes = set(path)
    for node in visited_nodes:
        stats["Steps"] += 1
        stats["Visited Nondes"] = len(visited_nodes)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000
        
        if callback:
            callback(node)
        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

    stats["Time (ms)"] = (time.time() - t0) * 1000
    return path, stats
