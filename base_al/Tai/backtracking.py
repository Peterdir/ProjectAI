def find_path(maze, start, goal):
    ROWS, COLS = len(maze), len(maze[0])
    path = []
    visited = set()

    def backtrack(x, y):
        if (x, y) == goal:
            return True
        dirs = [(-1,0),(1,0),(0,1),(0,-1)]
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if (0 <= nx < ROWS and 0 <= ny < COLS 
                and maze[nx][ny] == 0 
                and (nx, ny) not in visited):
                visited.add((nx, ny))
                path.append((nx, ny))
                if backtrack(nx, ny):
                    return True
                path.pop()
        return False

    visited.add(start)
    path.append(start)
    return path if backtrack(start[0], start[1]) else None


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
