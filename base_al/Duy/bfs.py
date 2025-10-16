from queue import Queue


def check_valid(r, c, R, C, maze, visited):
    return 0 <= r < R and 0 <= c < C and maze[r][c] == 0 and (r, c) not in visited

def find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    queue = Queue()
    queue.put(start)
    parent = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while not queue.empty():
        r, c = queue.get()

        if (r, c) == goal:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if check_valid(nr, nc, R, C, maze, parent):
                parent[(nr, nc)] = (r, c)
                queue.put((nr, nc))

    if goal not in parent:
        return None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    path.reverse()
    return path


# ----- TEST -----
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0]
]

start = (0, 0)
goal = (3, 4)

result = find_path(maze, start, goal)
print(result)