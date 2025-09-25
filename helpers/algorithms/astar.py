from queue import PriorityQueue

def check_valid(r, c, R, C, maze):
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    priorityQueue = PriorityQueue()
    g_start = 0
    f_start = heuristic(start, goal)
    parent = {start: None}
    priorityQueue.put((f_start, g_start, start))
    cost = {start: 0}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while not priorityQueue.empty():
        f_val, g_val, (r, c) = priorityQueue.get()
        if (r, c) == goal:
            break

        for dr, dc in dirs:
            nr, nc = dr + r, dc + c
            if check_valid(nr, nc, R, C, maze):
                new_g = g_val + 1
                if (nr, nc) not in cost or new_g < cost[(nr, nc)]:
                    cost[(nr, nc)] = new_g
                    parent[(nr, nc)] = (r, c)
                    new_f = new_g + heuristic((nr, nc), goal)
                    priorityQueue.put((new_f, new_g, (nr, nc)))

    if goal not in parent:
        return None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return list(reversed(path))
