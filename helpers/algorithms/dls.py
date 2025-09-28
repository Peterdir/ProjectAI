import time

def depth_limited_dfs(maze, start, goal, callback=None, update_callback=None, limit=200):
    R, C = len(maze), len(maze[0])
    stack = [(start, 0)]
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps = 0
    t0 = time.time()

    while stack:
        (r, c), depth = stack.pop()
        steps += 1

        stats = {
            "Steps": steps,
            "Visited nodes": len(prev),
            "Depth": depth,
            "Time (ms)": (time.time() - t0) * 1000
        }

        cur = (r, c)
        path_length = 0
        while cur:
            path_length += 1
            cur = prev[cur]
        stats["Path length"] = path_length

       

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if (r, c) == goal:
            return prev  # tìm được goal
        if depth >= limit:
            continue  # cắt nhánh quá sâu
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr,nc) not in prev:
                prev[(nr,nc)] = (r,c)
                stack.append(((nr,nc), depth+1))
                if callback:
                    callback((nr, nc))  # tô màu ô được mở rộng
    return prev if goal in prev else None

def find_path(maze, start, goal, callback=None, update_callback=None, limit=200):
    t0 = time.time()
    prev = depth_limited_dfs(maze, start, goal, callback, update_callback, limit)
    if not prev or goal not in prev:
        stats = {
            "Visited nodes": len(prev) if prev else 0,
            "Depth limit": limit,
            "Time (ms)": (time.time() - t0) * 1000
        }
        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))
        return None, stats

    path, cur = [], goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    path = list(reversed(path))
    stats = {
        "Visited nodes": len(prev),
        "Depth limit": limit,
        "Path length": len(path),
        "Time (ms)": (time.time() - t0) * 1000
    }
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))
    return path, stats
