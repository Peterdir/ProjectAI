from collections import deque
import time

def check_valid(r, c, R, C, maze, visited):
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0 and (r, c) not in visited

def find_path(maze, start, goal=None, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    if goal is None:
        goal = (R - 2, C - 2)

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    visited = set()
    path = []       # đường hiện tại
    steps = 0
    t0 = time.time()
    stats = {}

    def dfs(r, c):
        nonlocal steps, stats
        visited.add((r, c))
        path.append((r, c))
        steps += 1

        # Cập nhật stats
        stats = {
            "Steps": steps,
            "Visited nodes": len(visited),
            "Current node": (r, c),
            "Path length": len(path),
            "Time (ms)": (time.time() - t0) * 1000
        }

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))
        if callback:
            callback((r, c))

        # ĐÃ TỚI GOAL THẬT
        if (r, c) == goal:
            return True

        # Thử các hướng
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze, visited):
                if dfs(nr, nc):
                    return True

        # BACKTRACK – quay lui
        path.pop()         # gỡ node hiện tại khỏi đường đi
        return False       # báo là nhánh này tắc

    success = dfs(start[0], start[1])

    if success:
        return path, stats
    else:
        return None, stats