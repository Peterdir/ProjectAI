def depth_limited_dfs(maze, start, goal, callback, limit):
    R, C = len(maze), len(maze[0])
    stack = [(start, 0)]
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while stack:
        (r, c), depth = stack.pop()
        if (r, c) == goal:
            return prev  # tìm được goal
        if depth >= limit:
            continue  # cắt nhánh quá sâu
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr,nc) not in prev:
                prev[(nr,nc)] = (r,c)
                stack.append(((nr,nc), depth+1))

                if callback:
                    callback((nr, nc))  # tô màu ô được mở rộng
    return prev if goal in prev else None

def find_path(maze, start, goal, callback = None, limit=200):
    prev = depth_limited_dfs(maze, start, goal, callback, limit)
    if not prev or goal not in prev:
        return None

    path, cur = [], goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))
