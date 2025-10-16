import time

def check_valid(r, c, R, C, maze):
    """Kiểm tra ô (r, c) có nằm trong mê cung và không phải tường không."""
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

def heuristic(a, b):
    """Hàm heuristic: khoảng cách Manhattan giữa hai điểm a và b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_find_path(maze, start, goal):
    """
    Tìm đường đi bằng thuật toán Heuristic Search (Greedy Best-First Search).
    Luôn chọn node có giá trị heuristic (h) nhỏ nhất so với đích.
    
    Tham số:
        maze  : ma trận 2D (0: đường, 1: tường)
        start : tọa độ bắt đầu (r, c)
        goal  : tọa độ đích (r, c)

    Trả về:
        path  : danh sách các ô đi qua (nếu tìm được)
        stats : thống kê số bước, số node duyệt, thời gian
    """
    R, C = len(maze), len(maze[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    current_state = start
    current_heuristic = heuristic(start, goal)
    path = [start]
    steps = 0
    t0 = time.time()

    while True:
        steps += 1
        r, c = current_state
        neighbors = []

        # Tìm các ô láng giềng hợp lệ
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze):
                neighbors.append((nr, nc))

        # Nếu không còn hướng đi
        if not neighbors:
            break

        # Chọn ô có heuristic nhỏ nhất
        next_state = min(neighbors, key=lambda n: heuristic(n, goal))
        next_heuristic = heuristic(next_state, goal)

        # Nếu tiến gần hơn đích → đi tiếp
        if next_heuristic < current_heuristic:
            current_state = next_state
            current_heuristic = next_heuristic
            path.append(next_state)

            # Nếu đến đích thì dừng
            if current_state == goal:
                break
        else:
            # Không thể tiến gần hơn — bị kẹt tại cực trị địa phương
            break

    stats = {
        "Steps": steps,
        "Visited nodes": len(set(path)),
        "Path length": len(path),
        "Found": (current_state == goal),
        "Time (ms)": (time.time() - t0) * 1000
    }

    if current_state == goal:
        return path, stats
    else:
        return None, stats
