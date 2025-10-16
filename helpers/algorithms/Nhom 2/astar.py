from queue import PriorityQueue
import time

def check_valid(r, c, R, C, maze):
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    priorityQueue = PriorityQueue()
    g_start = 0
    f_start = heuristic(start, goal)
    parent = {start: None}
    priorityQueue.put((f_start, g_start, start))
    cost = {start: 0}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps = 0
    t0 = time.time()
    stats = {}

    while not priorityQueue.empty():
        f_val, g_val, (r, c) = priorityQueue.get()
        steps += 1

        # Path length hiện tại
        path_length = 0
        cur = (r, c)
        while cur is not None:
            path_length += 1
            cur = parent[cur]

        # Tính h_val
        h_val = f_val - g_val

        # stats đầy đủ
        stats = {
            "Steps": steps,
            "Visited nodes": len(cost),
            "Path length": path_length,
            "Current node": (r, c),
            "Frontier size": priorityQueue.qsize(),
            "f_val": f_val,
            "g_val": g_val,
            "h_val": h_val,
            "Time (ms)": (time.time() - t0) * 1000
        }

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if (r, c) == goal:
            break

        for dr, dc in dirs:
            nr, nc = dr + r, dc + c
            if check_valid(nr, nc, R, C, maze):
                new_g = g_val + 1
                if (nr, nc) not in cost or new_g < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_g
                    parent[(nr, nc)] = (r, c)
                    new_f = new_g + heuristic((nr, nc), goal)
                    priorityQueue.put((new_f, new_g, (nr, nc)))

                    if callback:
                        callback((nr, nc))

    # Nếu không tìm thấy goal, trả về None kèm stats cuối cùng
    if goal not in parent:
        return None, stats

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    return list(reversed(path)), stats
