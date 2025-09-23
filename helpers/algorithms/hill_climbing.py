def heuristic(a, b):
    """Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal, max_steps=10000):
    """Greedy Hill Climbing cải tiến với backtracking"""
    R, C = len(maze), len(maze[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    stack = [(start, [start])]  # (current_pos, path_so_far)
    visited = set([start])
    steps = 0

    while stack:
        if steps >= max_steps:
            return None
        steps += 1

        current, path = stack.pop()
        if current == goal:
            return path

        # lấy neighbors chưa visited, sắp xếp theo heuristic nhỏ nhất
        neighbors = []
        r, c = current
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc]==0 and (nr,nc) not in visited:
                neighbors.append((nr,nc))
        # sort neighbor theo heuristic
        neighbors.sort(key=lambda x: heuristic(x, goal))

        # đẩy neighbors vào stack (backtracking)
        for n in reversed(neighbors):  # reversed vì stack pop cuối vào đầu
            visited.add(n)
            stack.append((n, path + [n]))

    return None  # không tìm được
