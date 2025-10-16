import math

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

def negamax(maze, state, goal, visited):
    if state == goal:
        return 0, [state]  # điểm 0 vì đã đến đích

    best_score = math.inf
    best_path = None

    for move in get_moves(state, maze):
        if move not in visited:
            score, path = negamax(maze, move, goal, visited | {move})
            score = -score + 1  # phủ định điểm đối thủ (Negamax)

            if score < best_score:
                best_score = score
                best_path = [state] + path

    return best_score, best_path

def negamax_find_path(maze, start, goal):
    score, path = negamax(maze, start, goal, {start})
    return path
