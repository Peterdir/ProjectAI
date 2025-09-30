import heapq
import time

def find_path(maze, start, goal, callback = None, update_callback=None):
    """
    Uniform Cost Search (giống Dijkstra)
    - Luôn mở node có cost nhỏ nhất trước
    - Cost ở đây = số bước đã đi
    """
    rows, cols = len(maze), len(maze[0])
    frontier = [(0, start, [start])]  # (cost, node, path)
    visited = set()
    steps = 0
    t0 = time.time()
    stats = {}

    while frontier:
        cost, (x, y), path = heapq.heappop(frontier)
        steps += 1

        # Path length hiện tại
        path_length = len(path)

        # stats realtime
        stats = {
            "Steps": steps,
            "Visited nodes": len(visited),
            "Current node": (x, y),
            "Frontier size": len(frontier),
            "Path length": path_length,
            "Cost": cost,
            "Time (ms)": (time.time() - t0) * 1000
        }

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        # Nếu đến đích thì trả về đường đi
        if (x, y) == goal:
            return path, stats

        if (x, y) in visited:
            continue
        visited.add((x, y))

        # Gọi callback để tô màu ô được mở rộng
        if callback:
            callback((x, y))

        # Duyệt các ô kề
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                heapq.heappush(frontier, (cost + 1, (nx, ny), path + [(nx, ny)]))

    return None, stats  # Không tìm thấy đường

def cost():
    return 1
def find_path(maze, start, goal):
    ROWS = len(maze)
    COLS = len(maze[0])

    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, (x,y), path = heapq.pop()

        if (x,y) == goal:
            return path, cost
        
        if (x,y) in visited:
            continue
        visited.add((x,y))

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[0][0]:
                if (nx,ny) not in visited:
                    heapq.heappush(pq,(cost + 1, (nx,ny), path + [(nx,ny)]))
                
        
        return None, None # Bó tay

