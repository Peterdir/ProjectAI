import math
import time

def heuristic(state, goal):
    r, c = state
    gr, gc = goal
    return abs(r - gr) + abs(c - gc)

def get_moves(state, maze):
    R, C = len(maze), len(maze[0])
    r, c = state
    moves = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
            moves.append((nr, nc))
    return moves

def negamax_to_goal(maze, state, goal, visited):
    if state == goal:
        return 0, [state]

    best_score = math.inf
    best_path = None

    for move in get_moves(state, maze):
        if move not in visited or move == goal:
            score, path = negamax_to_goal(maze, move, goal, visited | {move})
            score += 1  # mỗi bước đi +1

            if score < best_score:
                best_score = score
                best_path = [state] + path

    return best_score, best_path

def find_path(maze, start, goal, callback=None, update_callback=None):
    t0 = time.time()
    score, path = negamax_to_goal(maze, start, goal, {start})

    if path is None:
        raise ValueError("Không tìm thấy đường đi đến goal")

    visited_nodes_in_path = set(path)
    stats = {
        "Steps": len(path),
        "Visited Nodes": len(visited_nodes_in_path),
        "Path length": len(path),
        "Time (ms)": (time.time() - t0) * 1000
    }

    if callback:
        for pos in path:
            callback(pos)

    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))

    return path, stats
