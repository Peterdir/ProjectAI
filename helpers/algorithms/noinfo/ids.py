import time

# Hướng di chuyển: lên, xuống, trái, phải
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Kiểm tra vị trí hợp lệ
def is_valid(maze, position):
    r, c = position
    return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0


# IDDFS (Iterative Deepening Depth-First Search) có callback và update_callback
def find_path(maze, start, goal, callback=None, update_callback=None, max_limit=1000):
    t0 = time.time()
    steps_ref = [0]  # đếm tổng số bước duyệt
    visited = set()  # để đếm visited nodes tổng cộng

    def dls(node, depth, path):
        steps_ref[0] += 1
        visited.add(node)

        # Cập nhật thông tin hiện tại
        if update_callback:
            stats = {
                "Steps": steps_ref[0],
                "Visited nodes": len(visited),
                "Depth": depth,
                "Current node": node,
                "Time (ms)": (time.time() - t0) * 1000,
            }
            update_callback(stats, highlight_keys=[k for k, v in stats.items() if v is not None])

        # Gọi callback mỗi khi thăm node
        if callback:
            callback(node)

        # Nếu đến đích thì trả về đường đi
        if node == goal:
            return path

        # Nếu hết độ sâu thì dừng
        if depth == 0:
            return None

        # Mở rộng các hướng
        for dr, dc in DIRECTIONS:
            nr, nc = node[0] + dr, node[1] + dc
            next_node = (nr, nc)
            if is_valid(maze, next_node) and next_node not in path:
                result = dls(next_node, depth - 1, path + [next_node])
                if result:
                    return result
        return None

    limit = 0
    while limit <= max_limit:
        result = dls(start, limit, [start])
        if result:
            # Khi tìm thấy đường đi
            stats = {
                "Steps": steps_ref[0],
                "Visited nodes": len(visited),
                "Depth limit": limit,
                "Path length": len(result),
                "Time (ms)": (time.time() - t0) * 1000,
            }
            if update_callback:
                update_callback(stats, highlight_keys=list(stats.keys()))
            return result, stats

        # Nếu chưa tìm thấy, tăng giới hạn độ sâu
        limit += 1

    # Nếu vượt quá giới hạn mà vẫn không tìm thấy
    stats = {
        "Steps": steps_ref[0],
        "Visited nodes": len(visited),
        "Depth limit": limit,
        "Time (ms)": (time.time() - t0) * 1000,
    }
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))
    return None, stats
