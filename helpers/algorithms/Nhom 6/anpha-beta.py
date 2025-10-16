import math

def find_path(maze, start, goal, callback=None, update_callback=None, max_depth=4):
    def heuristic(state):
        r, c = state
        gr, gc = goal
        return abs(r - gr) + abs(c - gc)
    
    def get_moves(state):
        r, c = state
        moves = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0:
                moves.append((nr, nc))
        return moves

    def is_terminal(state, depth):
        return depth == 0 or state == goal

    def alphabeta(state, depth, alpha, beta, maximizing):
        if is_terminal(state, depth):
            return -heuristic(state), state

        best_state = None
        if maximizing:  # agent move
            value = -math.inf
            for move in get_moves(state):
                score, _ = alphabeta(move, depth - 1, alpha, beta, False)
                if score > value:
                    value, best_state = score, move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_state
        else:  # opponent move (giả định gây bất lợi)
            value = math.inf
            for move in get_moves(state):
                # Giả định đối thủ chọn hướng xa goal nhất
                score, _ = alphabeta(move, depth - 1, alpha, beta, True)
                if score < value:
                    value, best_state = score, move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_state

    # --- main ---
    path = [start]
    current = start
    steps = 0
    visited = set()

    for depth in range(max_depth):
        steps += 1
        visited.add(current)
        _, next_state = alphabeta(current, max_depth, -math.inf, math.inf, True)
        if not next_state or next_state == goal:
            break
        path.append(next_state)
        current = next_state

        if update_callback:
            update_callback({
                "Steps": steps,
                "Visited nodes": len(visited),
                "Current position": current,
                "Path length": len(path)
            })

    if callback:
        for pos in path:
            callback(pos)

    return path, {
        "Steps": steps,
        "Visited nodes": len(visited),
        "Path length": len(path)
    }
