import math

def find_path(maze, start, goal, callback=None, update_callback=None, max_depth=5):
    
    def is_terminal(state, depth):
        r, c = state
        return state == goal or depth == 0

    def heuristic(state):
        r, c = state
        gr, gc = goal
        return abs(r - gr) + abs(c - gc)
    
    def get_moves(state):
        r, c = state
        moves = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0:
                moves.append((nr, nc))
        return moves

    def minimax(state, depth, maximizingPlayer):
        if is_terminal(state, depth):
            return -heuristic(state) if maximizingPlayer else heuristic(state), state
        
        best_state = None
        if maximizingPlayer:
            max_eval = -math.inf
            for move in get_moves(state):
                eval_score, _ = minimax(move, depth-1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_state = move
            return max_eval, best_state
        else:
            min_eval = math.inf
            for move in get_moves(state):
                eval_score, _ = minimax(move, depth-1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_state = move
            return min_eval, best_state

    # Bắt đầu từ start
    path = [start]
    current = start
    steps = 0
    visited_nodes = set()
    
    for depth_remaining in range(max_depth, 0, -1):
        steps += 1
        visited_nodes.add(current)
        _, next_state = minimax(current, depth_remaining, True)
        if next_state is None or next_state == goal:
            break
        path.append(next_state)
        current = next_state

        # Cập nhật metrics từng bước
        if update_callback:
            stats = {
                "Steps": steps,
                "Visited nodes": len(visited_nodes),
                "Current position": current,
                "Path length": len(path)
            }
            update_callback(stats)
    
    # Metrics cuối cùng
    final_stats = {
        "Steps": steps,
        "Visited nodes": len(visited_nodes),
        "Path length": len(path)
    }
    
    # Gọi callback cho từng vị trí trong path
    if callback:
        for pos in path:
            callback(pos)
    
    return path, final_stats
