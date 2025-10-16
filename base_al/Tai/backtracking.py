def cothediduoc(x, y, maze):
    COLS = len(maze[0])
    ROWS = len(maze)
    result = []
    dirs = [(-1,0),(0,-1),(1,0),(0,1)] # Điều hướng các hướng đi
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
            result.append((nx, ny))
    return result

def find_path(maze, start, goal):
    COLS = len(maze[0])
    ROWS = len(maze)
    path = []
    visited = set()

    def backtrack(x, y):
        # Kiểm tra trạng thái hiện tại có phải là goal không
        if (x, y) == goal:
            return True
        # Duyệt từng cặp tọa độ có thể đi được
        for nx, ny in cothediduoc(x, y, maze):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                path.append((nx, ny))
                if backtrack(nx, ny):
                    return True
                path.pop()
        return False

    visited.add(start)
    path.append(start)
    return path if backtrack(start[0], start[1]) else None


