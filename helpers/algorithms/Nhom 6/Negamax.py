import math
import time

def heuristic(state, goal):
    """Hàm heuristic: khoảng cách Manhattan"""
    r, c = state
    gr, gc = goal
    return abs(r - gr) + abs(c - gc)

def get_moves(state, maze):
    """Trả về danh sách các ô có thể đi tới (4 hướng)"""
    R, C = len(maze), len(maze[0])
    r, c = state
    moves = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
            moves.append((nr, nc))
    return moves

def negamax(maze, state, goal, visited, depth_limit=500):
    """
    Negamax có heuristic, có kiểm tra ngõ cụt và giới hạn độ sâu
    """
    # Điều kiện dừng
    if state == goal:
        return 0, [state]
    if len(visited) > depth_limit:
        return math.inf, None  # tránh vòng lặp vô hạn

    best_score = math.inf
    best_path = None

    for move in get_moves(state, maze):
        if move not in visited:
            score, path = negamax(maze, move, goal, visited | {move}, depth_limit)
            
            # Nếu không có đường đi từ move đến goal thì bỏ qua nhánh này
            if path is None:
                continue

            total_score = -score + heuristic(move, goal) + 1

            if total_score < best_score:
                best_score = total_score
                best_path = [state] + path

    # Nếu không tìm được đường đi nào hợp lệ
    if best_path is None:
        return math.inf, None

    return best_score, best_path

def find_path(maze, start, goal, callback=None, update_callback=None):
    """Hàm chính tìm đường dùng Negamax + Heuristic"""
    t0 = time.time()
    score, path = negamax(maze, start, goal, {start})

    if path is None:
        raise ValueError("Không tìm thấy đường đi đến goal")

    visited_nodes_in_path = set(path)
    stats = {
        "Steps": len(path),
        "Visited Nodes": len(visited_nodes_in_path),
        "Path Length": len(path),
        "Final Score": round(score, 2),
        "Time (ms)": round((time.time() - t0) * 1000, 3)
    }

    # Hiển thị từng bước đi nếu có callback
    if callback:
        for pos in path:
            callback(pos)

    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))

    return path, stats
