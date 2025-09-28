import heapq

def find_path(maze, start, goal, callback = None):
    """
    Uniform Cost Search (giống Dijkstra)
    - Luôn mở node có cost nhỏ nhất trước
    - Cost ở đây = số bước đã đi
    """
    rows, cols = len(maze), len(maze[0])
    frontier = [(0, start, [start])]  # (cost, node, path)
    visited = set()

    while frontier:
        cost, (x, y), path = heapq.heappop(frontier)

        # Nếu đến đích thì trả về đường đi
        if (x, y) == goal:
            return path

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

    return None  # Không tìm thấy đường
