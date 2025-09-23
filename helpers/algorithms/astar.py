import heapq

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    pq = [(0, start)]  # (priority, node)
    g_score = {start: 0}
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while pq:
        _, (r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            break
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
                new_g = g_score[(r,c)] + 1
                if (nr,nc) not in g_score or new_g < g_score[(nr,nc)]:
                    g_score[(nr,nc)] = new_g
                    f_score = new_g + heuristic((nr,nc), goal)
                    heapq.heappush(pq, (f_score, (nr,nc)))
                    prev[(nr,nc)] = (r,c)

    if goal not in prev:
        return None

    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))
