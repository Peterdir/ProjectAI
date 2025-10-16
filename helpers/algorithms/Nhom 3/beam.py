import heapq
import time

def heuristic(node, goal):
    x, y = node
    gx, gy = goal
    return abs(x - gx) + abs(y - gy)

def find_path(maze, start, goal, callback=None, update_callback=None, beam_width=3):
    ROWS, COLS = len(maze), len(maze[0])
    frontier = [(heuristic(start, goal), start, [start])]
    visited = set()
    steps = 0
    t0 = time.time()
    stats = {}

    while frontier:
        # Giữ lại beam_width ứng viên tốt nhất
        frontier = heapq.nsmallest(beam_width, frontier)
        new_frontier = []

        for score, (x, y), path in frontier:
            steps += 1

            # stats realtime
            stats = {
                "Steps": steps,
                "Visited nodes": len(visited),
                "Current node": (x, y),
                "Frontier size": len(frontier),
                "Path length": len(path),
                "Heuristic": score,
                "Time (ms)": (time.time() - t0) * 1000
            }
            if update_callback:
                update_callback(stats, highlight_keys=list(stats.keys()))

            if (x, y) == goal:
                return path, stats

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                    if (nx, ny) in visited:
                        continue
                    new_path = path + [(nx, ny)]
                    new_score = heuristic((nx, ny), goal)
                    new_frontier.append((new_score, (nx, ny), new_path))

                    if callback:
                        callback((nx, ny))

        frontier = sorted(new_frontier, key=lambda x: x[0])

    # Nếu không tìm thấy goal
    return None, stats
