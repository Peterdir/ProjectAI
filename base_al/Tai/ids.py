# Hướng di chuyển: lên, xuống, trái, phải
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Kiểm tra vị trí hợp lệ
def is_valid(maze, position):
    r, c = position
    return 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] == 0

# IDDFS: Iterative Deepening Depth-First Search
def find_path(maze, start, goal):
    def dls(node, depth, path):
        if node == goal:
            return path
        if depth == 0:
            return None
        
        for dr, dc in DIRECTIONS:
            nr, nc = node[0] + dr, node[1] + dc
            next_node = (nr, nc)
            if is_valid(maze, next_node) and next_node not in path:
                result = dls(next_node, depth - 1, path + [next_node])
                if result:
                    return result
        return None

    depth = 0
    while True:
        result = dls(start, depth, [start])
        if result:
            return result
        depth += 1
