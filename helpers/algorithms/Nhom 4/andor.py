import time

def find_path(maze, start, goal, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    steps = 0
    visited = set()
    t0 = time.time()
    stats = {}

    def check_valid(r, c, parent):
        return 0 <= r < R and 0 <= c < C and maze[r][c] == 0 and (r, c) not in parent

    def search(state, path):
        nonlocal steps
        steps += 1
        r, c = state
        path = path + [state]
        visited.add(state)

        stats.update({
            "Steps": steps,
            "Visited nodes": len(visited),
            "Current node": state,
            "Path length": len(path),
            "Time (ms)": (time.time() - t0) * 1000
        })

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        if callback:
            callback(state)

        if state == goal:
            return path

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, visited):
                result = search((nr, nc), path)
                if result:  
                    return result

        return None

    solution_path = search(start, [])
    return list(solution_path), stats