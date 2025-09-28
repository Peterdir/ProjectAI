import time

def find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    stack = [start]
    prev = {start: None}
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]

    steps = 0  # số bước (số lần pop từ stack)
    t0 = time.perf_counter()

    while stack:
        r, c = stack.pop()
        steps += 1
        if (r, c) == goal:
            break
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr, nc) not in prev:
                prev[(nr, nc)] = (r, c)
                stack.append((nr, nc))

    # reconstruct path if found
    path = None
    if goal in prev:
        path = []
        cur = goal
        while cur:
            path.append(cur)
            cur = prev[cur]
        path = list(reversed(path))

    t1 = time.perf_counter()

    # metrics
    visited_nodes = len(prev)
    path_len = (len(path) - 1) if path else 0
    runtime_ms = (t1 - t0) * 1000.0

    return {
        "path": path,
        "metrics": {
            "steps": steps,
            "visited_nodes": visited_nodes,
            "path_length": path_len,
            "runtime_ms": runtime_ms,
        },
    }
