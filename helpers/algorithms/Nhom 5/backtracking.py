import time

def cothediduoc(x, y, maze):
    COLS = len(maze[0])
    ROWS = len(maze)
    result = []
    dirs = [(-1,0),(0,-1),(1,0),(0,1)]  # lên, trái, xuống, phải
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
            result.append((nx, ny))
    return result


def find_path(maze, start, goal, callback=None, update_callback=None):
    COLS = len(maze[0])
    ROWS = len(maze)
    path = []
    visited = set()
    stats = {"Steps": 0, "Visited nodes": 0, "Path length": 0, "Time (ms)": 0.0}

    t0 = time.time()

    def backtrack(x, y):
        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if (x, y) == goal:
            return True

        for nx, ny in cothediduoc(x, y, maze):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                path.append((nx, ny))

                if callback:
                    callback((nx, ny))

                if backtrack(nx, ny):
                    return True

                path.pop()
                visited.remove((nx, ny))

        return False

    visited.add(start)
    path.append(start)

    found = backtrack(start[0], start[1])
    stats["Time (ms)"] = (time.time() - t0) * 1000

    return (path, stats) if found else (None, stats)
