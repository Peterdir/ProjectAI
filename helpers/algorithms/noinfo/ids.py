import time

def depth_limited_dfs(maze, start, goal, callback, limit, update_callback=None, t0=None, steps_ref=None):
    R, C = len(maze), len(maze[0])
    stack = [(start, 0)]
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while stack:
        (r, c), depth = stack.pop()
        if steps_ref is not None:
            steps_ref[0] += 1

        # live metrics
        if update_callback:
            stats = {
                "Steps": steps_ref[0] if steps_ref is not None else None,
                "Visited nodes": len(prev),
                "Depth": depth,
                "Current node": (r, c),
                "Time (ms)": ((time.time()-t0)*1000) if t0 else None,
            }
            update_callback(stats, highlight_keys=[k for k,v in stats.items() if v is not None])

        if callback:
            callback((r, c))  # Gọi callback mỗi khi ô được thăm
            
        if (r, c) == goal:
            return prev
        if depth < limit:
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr,nc) not in prev:
                    prev[(nr,nc)] = (r,c)
                    stack.append(((nr,nc), depth+1))
    return None

def find_path(maze, start, goal, callback = None, update_callback=None, max_limit=1000):
    limit = 0
    t0 = time.time()
    steps_ref = [0]
    stats = {}
    while True:
        prev = depth_limited_dfs(maze, start, goal, callback, limit, update_callback, t0, steps_ref)
        if prev and goal in prev:
            path, cur = [], goal
            while cur:
                path.append(cur)
                cur = prev[cur]
            path = list(reversed(path))
            stats = {
                "Steps": steps_ref[0],
                "Visited nodes": len(prev),
                "Depth limit": limit,
                "Path length": len(path),
                "Time (ms)": (time.time()-t0)*1000
            }
            if update_callback:
                update_callback(stats, highlight_keys=list(stats.keys()))
            return path, stats
        limit += 1
        if limit > max_limit:  # tránh vòng lặp vô hạn
            stats = {
                "Steps": steps_ref[0],
                "Visited nodes": len(prev) if prev else 0,
                "Depth limit": limit,
                "Time (ms)": (time.time()-t0)*1000
            }
            if update_callback:
                update_callback(stats, highlight_keys=list(stats.keys()))
            return None, stats
