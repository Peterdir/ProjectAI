def find_path(maze, start, goal, callback = None):
    ROWS = len(maze)
    COLS = len(maze[0])

    stack = [(start, [start])]
    visited = set() # Dùng set để không bị trùng các ô đã qua

    while stack:
        (x,y), path = stack.pop() # Lấy ô có tọa độ x và y trong path để xét

        if (x,y) == goal:
            return path
        if (x,y) in visited:
            continue

        visited.add((x, y))


        # Di chuyển theo 4 hướng: lên, xuống, trái, phải
        for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0: # Kiểm tra sau khi di chuyển thì nhân vật có còn nằm trong mê cung không
                stack.append(((nx, ny), path +[(nx, ny)]))

                # Gọi callback khi ô được mở rộng
                if callback:
                    callback((nx, ny))

    return None
