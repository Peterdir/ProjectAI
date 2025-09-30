import time

def find_path(maze, start, goal, callback=None, update_callback=None):
    ROWS, COLS = len(maze), len(maze[0])
    stack = [(start, [start])]
    visited = set()

    stats = {"Steps": 0, "Visited nodes": 0, "Path length": 0, "Time (ms)": 0.0}
    t0 = time.time()

    while stack:
        (x, y), path = stack.pop()
        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback:
            # highlight tất cả để update real-time
            update_callback(stats, highlight_keys=list(stats.keys()))

        if (x, y) == goal:
            return path, stats

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                stack.append(((nx, ny), path + [(nx, ny)]))
                if callback:
                    callback((nx, ny))

    # cuối cùng nếu không tìm thấy
    stats["Visited nodes"] = len(visited)
    stats["Time (ms)"] = (time.time() - t0) * 1000
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))
    return None, stats

def find_path(maze, start, goal):
    ROWS = len(maze)
    COLS = len(maze[0])

    stack = [(start, [start])]
    visited = set() # Dùng set để không bị trùng các ô đã qua

    while stack:
        (x,y), path = stack.pop() # Lấy ô có tọa độ x và y trong path để xét

        if (x,y) == goal:
            return path
        if (x,y) in visited:
            continue

        visited.add(x,y)

    # Di chuyển theo 4 hướng: lên, xuống, trái, phải
    for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0: # Kiểm tra sau khi di chuyển thì nhân vật có còn nằm trong mê cung không
            stack.append(((nx, ny), path +[(nx, ny)]))

    return None  # Bó tay

