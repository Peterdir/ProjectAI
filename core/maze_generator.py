import numpy as np

def generate_random_maze(rows, cols, seed=None):
    """
    Sinh ra một mê cung ngẫu nhiên bằng thuật toán Recursive Backtracking.
    Trả về: (maze_data, start_pos, goal_pos, used_seed)
    """
    if seed is None:
        seed = np.random.randint(0, 10**9)
    np.random.seed(seed)

    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_passages_from(r, c):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        np.random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr * 2, c + dc * 2
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                maze[r + dr][c + dc] = 0
                maze[nr][nc] = 0
                carve_passages_from(nr, nc)

    # Bắt đầu carving từ (0, 0)
    maze[0][0] = 0
    carve_passages_from(0, 0)

    # Tạo thêm các đường phụ ngẫu nhiên để thoáng hơn
    extra_paths = int(rows * cols * 0.15) # Tăng tỷ lệ một chút cho thú vị
    for _ in range(extra_paths):
        r, c = np.random.randint(1, rows - 1), np.random.randint(1, cols - 1)
        if maze[r][c] == 1:
            # Đếm số ô trống xung quanh
            neighbors = 0
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if maze[r + dr][c + dc] == 0:
                    neighbors += 1
            # Chỉ đục tường nếu nó nối 2 khu vực riêng biệt (có 2 ô trống)
            if neighbors == 2:
                maze[r][c] = 0

    start_pos = (0, 0)
    goal_pos = (rows - 1, cols - 1)
    maze[start_pos[0]][start_pos[1]] = 0
    maze[goal_pos[0]][goal_pos[1]] = 0

    return maze, start_pos, goal_pos, seed