import time

def heuristic(vitri, goal):
    x, y = vitri
    gx, gy = goal
    return abs(x - gx) + abs(y - gy)


def minimax_dfs(maze, current, goal, depth, is_maximizing, visited):
    # Nếu hết độ sâu hoặc đã tới đích
    if depth == 0 or current == goal:
        # Minimax sẽ tối ưu điểm: càng gần goal thì điểm càng cao
        return -heuristic(current, goal), [current]

    visited.add(current)
    moves = []
    ROWS = len(maze)
    COLS = len(maze[0])
    x, y = current

    # 4 hướng di chuyển
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
            moves.append((nx, ny))

    # Nếu không còn nước đi
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



def find_path(maze, start=None, goal=None, callback=None, update_callback=None):
    ROWS = len(maze)
    COLS = len(maze[0])

    # Xác định START & GOAL chính xác
    if start is None:
        start = (12, 18)  # tránh tường ngoài nếu có border

    if goal is None:
        goal = (ROWS - 2, COLS - 2)  # vị trí cuối thật

    stats = {
        "Steps": 0,
        "Visited Nodes": 0,
        "Path length": 0,
        "Time (ms)": 0
    }

    t0 = time.time()
    MAX_DEPTH = 200  # tăng nếu mê cung lớn

    score, path = minimax_dfs(maze, start, goal, MAX_DEPTH, True, set())

    visited_nodes = set(path)

    for node in visited_nodes:
        stats["Steps"] += 1
        stats["Visited Nodes"] = len(visited_nodes)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if callback:
            callback(node)
        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

    stats["Time (ms)"] = (time.time() - t0) * 1000
    return path, stats