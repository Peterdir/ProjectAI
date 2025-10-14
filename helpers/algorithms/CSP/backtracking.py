import time

def find_path(maze, start, goal, callback=None, update_callback=None):
    ROWS, COLS = len(maze), len(maze[0])
    visited = set()
    path = []

    stats = {"Steps": 0, "Visited nodes": 0, "Path length": 0, "Time (ms)": 0.0}
    t0 = time.time()

    def backtrack(x, y):
        dirs=[(-1,0),(1,0),(0,1),(0,-1)]
        # update stats
        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        # check goal
        if (x, y) == goal:
            return True

        # thử tất cả hướng
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                path.append((nx, ny))

                if callback:
                    callback((nx, ny))

                if backtrack(nx, ny):
                    return True
                path.pop()
                visited.remove((nx, ny))

        return False

    # khởi tạo
    visited.add(start)
    path.append(start)

    if backtrack(start[0], start[1]):
        stats["Time (ms)"] = (time.time() - t0) * 1000
        return path, stats

    stats["Time (ms)"] = (time.time() - t0) * 1000
    return None, stats