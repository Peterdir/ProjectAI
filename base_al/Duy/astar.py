from queue import PriorityQueue
import time

def check_valid(r, c, R, C, maze):
    """Kiểm tra ô (r, c) có nằm trong mê cung và không phải tường không."""
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

def heuristic(a, b):
    """Hàm heuristic: khoảng cách Manhattan giữa 2 điểm a và b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_find_path(maze, start, goal):
    """
    Tìm đường đi trong mê cung bằng thuật toán A* (A-star).
    
    Tham số:
        maze  : ma trận 2D (0: đường, 1: tường)
        start : tọa độ bắt đầu (r, c)
        goal  : tọa độ đích (r, c)

    Trả về:
        path  : danh sách các ô tạo thành đường đi từ start → goal
        stats : thống kê (bước, node thăm, chi phí, thời gian)
    """
    R, C = len(maze), len(maze[0])
    pq = PriorityQueue()
    g_start = 0
    f_start = heuristic(start, goal)
    pq.put((f_start, g_start, start))

    parent = {start: None}
    cost = {start: 0}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    steps = 0
    t0 = time.time()

    while not pq.empty():
        f_val, g_val, (r, c) = pq.get()
        steps += 1

        # Nếu đến đích thì dừng
        if (r, c) == goal:
            break

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze):
                new_g = g_val + 1
                new_f = new_g + heuristic((nr, nc), goal)
                if (nr, nc) not in cost or new_g < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_g
                    parent[(nr, nc)] = (r, c)
                    pq.put((new_f, new_g, (nr, nc)))

    # Nếu không tìm thấy đường
    if goal not in parent:
        stats = {
            "Steps": steps,
            "Visited nodes": len(cost),
            "Found": False,
            "Time (ms)": (time.time() - t0) * 1000
        }
        return None, stats

    # Truy ngược để dựng lại đường đi
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    stats = {
        "Steps": steps,
        "Visited nodes": len(cost),
        "Path length": len(path),
        "Found": True,
        "Time (ms)": (time.time() - t0) * 1000
    }

    return path, stats
