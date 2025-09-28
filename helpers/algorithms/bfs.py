from collections import deque
from queue import Queue

def check_valid(r, c, R, C, maze, parent):
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0 and (r, c) not in parent

def find_path(maze, start, goal, callback = None):
    R, C = len(maze), len(maze[0])
    queue = Queue()
    queue.put(start)
    parent = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while not queue.empty():
        r, c = queue.get()

        # --- gọi callback để tô màu ô đang mở rộng ---
        if callback:
            callback((r, c))

        if(r, c) == goal:
            break

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze, parent):
                parent[(nr, nc)] = (r, c)
                queue.put((nr, nc))

    if goal not in parent:
        return None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    return list(reversed(path))
