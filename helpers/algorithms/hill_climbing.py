
def check_valid(r, c, R, C, maze):
    return 0 <= r < R and 0 <= c <= C and maze[r][c] == 0


def heuristic(a, b):
    """Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal, callback = None):
    R, C = len(maze), len(maze[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    current_state = start
    current_heuristic = heuristic(start, goal)
    path = [start]

    while True:
        r, c = current_state
        neighbors = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze):
                neighbors.append((nr, nc))

                if callback:
                    callback((nr, nc))  # tô màu ô đang được xét

        if not neighbors:
            # Không có láng giềng hợp lệ
            break

        next_state = min(neighbors, key=lambda n: heuristic(n, goal))
        next_heuristic = heuristic(next_state, goal)

        if next_heuristic < current_heuristic:
            path.append(next_state)
            current_state = next_state
            current_heuristic = next_heuristic
        else:
            break

    return path if current_state == goal else None