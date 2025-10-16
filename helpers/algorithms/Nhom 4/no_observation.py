from queue import Queue
import time

def check_valid(r, c, R, C, maze, parent):
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0 and (r, c) not in parent

def find_path(maze, start, goal=None, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    queue = Queue()
    queue.put(start)
    parent = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps = 0
    t0 = time.time()
    stats = {}

    # Lưu node xa nhất
    farthest_node = start
    max_depth = 1

    while not queue.empty():
        r, c = queue.get()
        steps += 1

        # Tính chiều dài đường hiện tại (depth)
        path_length = 0
        cur = (r, c)
        while cur is not None:
            path_length += 1
            cur = parent[cur]

        # Cập nhật node xa nhất nếu phát hiện node sâu hơn
        if path_length > max_depth:
            max_depth = path_length
            farthest_node = (r, c)

        # Cập nhật thống kê
        stats = {
            "Steps": steps,
            "Visited nodes": len(parent),
            "Current node": (r, c),
            "Queue size": queue.qsize(),
            "Path length": path_length,
            "Time (ms)": (time.time() - t0) * 1000
        }

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if callback:
            callback((r, c))

        # Blind mở rộng
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze, parent):
                parent[(nr, nc)] = (r, c)
                queue.put((nr, nc))

    # Sau khi đi hết map → trích node xa nhất làm goal
    goal = farthest_node
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    return list(reversed(path)), stats