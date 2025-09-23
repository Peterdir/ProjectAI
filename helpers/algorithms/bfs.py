from collections import deque

def find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    q = deque([start])
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while q:
        r, c = q.popleft()
        if (r, c) == goal:
            break
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr,nc) not in prev:
                prev[(nr,nc)] = (r,c)
                q.append((nr,nc))

    if goal not in prev:
        return None

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))
