import math
import time
import random

# Hàm heuristic: khoảng cách Manhattan
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, maze):
    R, C = len(maze), len(maze[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []
    for dr, dc in dirs:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors

# Hàm Alpha-Beta chính
def alpha_beta(maze, player, enemy, goal, depth, alpha, beta, maximizing):
    # Điều kiện dừng
    if player == goal:
        return 1000 - depth  # thưởng lớn khi tới đích
    if depth == 0:
        # giá trị càng nhỏ càng xa đích
        return -heuristic(player, goal) + heuristic(enemy, player) * -0.5

    if maximizing:
        max_eval = -math.inf
        for move in get_neighbors(player, maze):
            eval = alpha_beta(maze, move, enemy, goal, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_neighbors(enemy, maze):
            eval = alpha_beta(maze, player, move, goal, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_path(maze, start, goal, callback=None, update_callback=None):
    """
    Mô phỏng tìm đường bằng thuật toán Alpha–Beta pruning giữa người chơi và đối thủ.
    """
    R, C = len(maze), len(maze[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    t0 = time.time()

    # Vị trí khởi tạo của người chơi & đối thủ (đặt ngẫu nhiên trên ô trống)
    player = start
    free_cells = [(r,c) for r in range(R) for c in range(C) if maze[r][c] == 0 and (r,c) != start and (r,c) != goal]
    enemy = random.choice(free_cells)

    parent = {player: None}
    steps = 0

    # Mô phỏng lượt đi xen kẽ giữa Player (Max) và Enemy (Min)
    while player != goal and steps < 300:
        steps += 1

        # Gọi callback để hiển thị
        if callback:
            callback(player)

        # Cập nhật thống kê
        stats = {
            "Steps": steps,
            "Player": player,
            "Enemy": enemy,
            "Alpha": "-",
            "Beta": "-",
            "Time (ms)": (time.time() - t0) * 1000
        }
        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        # --- Lượt của người chơi (Max) ---
        best_score = -math.inf
        best_move = None
        for move in get_neighbors(player, maze):
            score = alpha_beta(maze, move, enemy, goal, 3, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_move = move

        if best_move:
            parent[best_move] = player
            player = best_move

        # --- Lượt của đối thủ (Min) ---
        enemy_moves = get_neighbors(enemy, maze)
        if enemy_moves:
            enemy = random.choice(enemy_moves)  # có thể làm "thông minh" hơn nếu cần

        if player == enemy:  # bị chặn
            break

    # reconstruct path
    if player != goal:
        return None, stats

    path = []
    cur = player
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    stats["Path length"] = len(path)
    stats["Visited nodes"] = len(parent)
    return path, stats
