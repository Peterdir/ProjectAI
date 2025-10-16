from queue import Queue
import time

def check_valid(r, c, R, C, maze, visited):
    """Kiểm tra ô (r, c) có hợp lệ hay không"""
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0 and (r, c) not in visited

def bfs_find_path(maze, start, goal):
    """
    Tìm đường đi trong mê cung bằng thuật toán BFS (Breadth-First Search).
    
    Tham số:
        maze  : ma trận 2D (0: đường, 1: tường)
        start : tọa độ bắt đầu (r, c)
        goal  : tọa độ đích (r, c)
    
    Trả về:
        path  : danh sách các ô từ start → goal
        stats : thông tin thống kê (số bước, số nút duyệt, thời gian, v.v.)
    """
    R, C = len(maze), len(maze[0])
    queue = Queue()
    queue.put(start)
    parent = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    steps = 0
    t0 = time.time()

    while not queue.empty():
        r, c = queue.get()
        steps += 1

        # Nếu đã đến đích, dừng tìm kiếm
        if (r, c) == goal:
            break

        # Duyệt 4 hướng
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze, parent):
                parent[(nr, nc)] = (r, c)
                queue.put((nr, nc))

    # Nếu goal không nằm trong parent → không tìm thấy đường
    if goal not in parent:
        stats = {
            "Steps": steps,
            "Visited nodes": len(parent),
            "Found": False,
            "Time (ms)": (time.time() - t0) * 1000
        }
        return None, stats

    # Truy vết lại đường đi từ goal về start
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    path.reverse()

    # Thống kê kết quả
    stats = {
        "Steps": steps,
        "Visited nodes": len(parent),
        "Path length": len(path),
        "Found": True,
        "Time (ms)": (time.time() - t0) * 1000
    }

    return path, stats
