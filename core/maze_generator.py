import numpy as np

def generate_random_maze(rows, cols, seed=None):
    """
    Sinh mê cung ngẫu nhiên bằng thuật toán Recursive Backtracking.
    Đảm bảo start và goal luôn nằm trên ô trống và có lối đi ra/vào.
    Trả về: (maze, start_pos, goal_pos, used_seed)
    """
    # ---- 1. Khởi tạo seed ----
    if seed is None:
        seed = np.random.randint(0, 10**9)
    rng = np.random.default_rng(seed)

    # ---- 2. Khởi tạo toàn bộ là tường ----
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    # ---- 3. Hàm đệ quy đào đường ----
    def carve_passages_from(r, c):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        rng.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr * 2, c + dc * 2
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                maze[r + dr][c + dc] = 0
                maze[nr][nc] = 0
                carve_passages_from(nr, nc)

    # ---- 4. Bắt đầu từ ô ngẫu nhiên (để đa dạng hơn) ----
    start_r = rng.integers(0, rows // 2)
    start_c = rng.integers(0, cols // 2)
    maze[start_r][start_c] = 0
    carve_passages_from(start_r, start_c)

    # ---- 5. Thêm các đường phụ ngẫu nhiên (cho thoáng hơn) ----
    extra_paths = int(rows * cols * 0.15)
    for _ in range(extra_paths):
        r, c = rng.integers(1, rows - 1), rng.integers(1, cols - 1)
        if maze[r][c] == 1:
            neighbors = sum(
                1 for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                if maze[r + dr][c + dc] == 0
            )
            if neighbors >= 2:
                maze[r][c] = 0

    # ---- 6. Đặt start & goal ----
    start_pos = (0, 0)
    goal_pos = (rows - 1, cols - 1)

    # Đảm bảo start và goal không phải tường
    maze[start_pos[0]][start_pos[1]] = 0
    maze[goal_pos[0]][goal_pos[1]] = 0

    # ---- 7. Mở lối xung quanh goal (tránh bị kín) ----
    gr, gc = goal_pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        rr, cc = gr + dr, gc + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            maze[rr][cc] = 0

    # ---- 8. Đảm bảo start cũng có ít nhất 1 lối ra ----
    sr, sc = start_pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        rr, cc = sr + dr, sc + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            maze[rr][cc] = 0

    return maze, start_pos, goal_pos, seed
