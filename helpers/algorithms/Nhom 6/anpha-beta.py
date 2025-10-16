import math

def find_path(maze, start, goal, callback=None, update_callback=None, max_depth=12):
    def heuristic(state):
        r, c = state
        gr, gc = goal
        return abs(r - gr) + abs(c - gc)  # Manhattan

    def get_moves(state):
        r, c = state
        moves = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0:
                moves.append((nr, nc))
        return moves

    def alphabeta(state, depth, alpha, beta, maximizing, path):
        # Nếu đạt mục tiêu hoặc hết độ sâu → kết thúc, trả path
        if state == goal or depth == 0:
            return -heuristic(state), path + [state]

        if maximizing:  # Agent (người tìm đường)
            best_score = -math.inf
            best_path = None
            for move in get_moves(state):
                score, new_path = alphabeta(move, depth - 1, alpha, beta, False, path + [state])
                if score > best_score:
                    best_score = score
                    best_path = new_path
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_path

        else:  # Opponent (giả lập cản đường)
            worst_score = math.inf
            worst_path = None
            for move in get_moves(state):
                score, new_path = alphabeta(move, depth - 1, alpha, beta, True, path + [state])
                if score < worst_score:
                    worst_score = score
                    worst_path = new_path
                beta = min(beta, worst_score)
                if alpha >= beta:
                    break
            return worst_score, worst_path

    # MAIN EXECUTION
    score, best_path = alphabeta(start, max_depth, -math.inf, math.inf, True, [])

    if not best_path:
        return [], {"Steps": 0, "Visited nodes": 0, "Path length": 0}

    visited = set(best_path)
    steps = len(best_path)

    # Gọi callback để vẽ GUI mê cung (tkinter)
    if callback:
        for pos in best_path:
            callback(pos)

    # Gửi thông tin ra Sidebar
    if update_callback:
        update_callback({
            "Steps": steps,
            "Visited nodes": len(visited),
            "Path length": len(best_path)
        })

    return best_path, {
        "Steps": steps,
        "Visited nodes": len(visited),
        "Path length": len(best_path)
    }
