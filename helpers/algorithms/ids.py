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
                nr, nc = r+dr, c+dc
                if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr,nc) not in prev:
                    prev[(nr,nc)] = (r,c)
                    stack.append(((nr,nc), depth+1))
    return None

def find_path(maze, start, goal):
    limit = 0
    while True:
        prev = depth_limited_dfs(maze, start, goal, limit)
        if prev and goal in prev:
            path, cur = [], goal
            while cur:
                path.append(cur)
                cur = prev[cur]
            return list(reversed(path))
        limit += 1
        if limit > 1000:  # tránh vòng lặp vô hạn
            return None
