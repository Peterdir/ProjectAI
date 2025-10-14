def depth_limited_dfs(maze, start, goal, limit):
    R, C = len(maze), len(maze[0])
    stack = [(start, 0)]
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while stack:
        (r, c), depth = stack.pop()
        if (r, c) == goal:
            return prev
        if depth < limit:
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr, nc) not in prev:
                    prev[(nr, nc)] = (r, c)
                    stack.append(((nr, nc), depth + 1))
    return None


def find_path(maze, start, goal, max_limit=1000):
    for limit in range(max_limit + 1):
        prev = depth_limited_dfs(maze, start, goal, limit)
        if prev is not None:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            return list(reversed(path))
    return None


# ----- TEST -----
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0]
]
start = (0, 0)
goal = (3, 4)

path = find_path(maze, start, goal)
print(path)
