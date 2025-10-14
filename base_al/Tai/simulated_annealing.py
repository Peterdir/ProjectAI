import math, random

def get_neibor(pos, maze, visited):
    R, C = len(maze), len(maze[0])
    x_cur, y_cur = pos
    neighbors = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x_cur + dx, y_cur + dy
        if 0 <= nx < R and 0 <= ny < C and maze[nx][ny] == 0 and (nx, ny) not in visited:
            neighbors.append((nx, ny))
    return neighbors

def h(state, goal):
    sx, sy = state
    gx, gy = goal
    return abs(sx - gx) + abs(sy - gy)

def xac_suat(cur_cost, new_cost, temperature):
    delta = cur_cost - new_cost
    if delta > 0:
        return 1.0  # Nếu bước mới tốt hơn -> chắc chắn nhận
    return math.exp(delta / temperature)  # Xác suất nhận bước tệ hơn

def find_path(maze, start, goal, alpha=0.99, min_temp=0.001, max_steps=5000):
    R, C = len(maze), len(maze[0])
    current = start
    visited = set([start])
    path = [start]
    steps = 0
    temperature=1
    while temperature > min_temp and steps < max_steps:
        steps += 1
        neighbors = get_neibor(current, maze, visited)

        # Nếu không còn bước đi -> backtrack
        if not neighbors:
            if len(path) > 1:
                path.pop()          # quay lại ô trước
                current = path[-1]  # đặt current về ô trước đó
                continue
            else:
                return None  # không có đường

        next_pos = random.choice(neighbors)
        current_e = h(current, goal)
        next_e = h(next_pos, goal)

        if random.random() < xac_suat(current_e, next_e, temperature):
            current = next_pos
            visited.add(current)
            path.append(current)
            if current == goal:
                return path
        temperature*=alpha

    return None

# ----- TEST -----
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0]
]
start = (0, 0)
goal = (3, 4)
path = find_path(maze, start, goal)
print(path)