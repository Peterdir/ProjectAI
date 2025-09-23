import heapq

def find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    pq = [(0, start)]
    cost = {start: 0}
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while pq:
        g, (r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            break
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
                new_cost = g + 1
                if (nr,nc) not in cost or new_cost < cost[(nr,nc)]:
                    cost[(nr,nc)] = new_cost
                    prev[(nr,nc)] = (r,c)
                    heapq.heappush(pq, (new_cost, (nr,nc)))

    if goal not in prev:
        return None

    path, cur = [], goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))
