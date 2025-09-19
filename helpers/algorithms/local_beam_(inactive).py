import random
from heapq import nlargest

def heuristic(a, b):
    """Hàm heuristic tính khoảng cách Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path(maze, start, goal, k=5, max_steps=20000, backtrack_steps=3, restart_rate=0.1):
    """
    Local Beam Search cải tiến nhẹ.
    Hàm này sẽ được gọi từ một luồng riêng, nên nó chỉ cần trả về kết quả.
    """
    R, C = len(maze), len(maze[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # (score, current_pos, path_list, visited_set)
    beams = [(start, [start], {start})]
    steps = 0

    while steps < max_steps:
        steps += 1
        all_candidates = []

        for current, path, visited in beams:
            r, c = current
            if current == goal:
                return path  # Trả về đường đi khi tìm thấy

            # Lấy các hàng xóm hợp lệ và chưa đi qua
            neighbors = [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < R and 0 <= c + dc < C and maze[r + dr][c + dc] == 0]
            valid_neighbors = [n for n in neighbors if n not in visited]

            # Nếu không có hàng xóm mới, xử lý backtracking hoặc restart
            if not valid_neighbors:
                # Backtrack
                if len(path) > backtrack_steps:
                    new_pos = path[-(backtrack_steps + 1)]
                    new_path = path[:-backtrack_steps]
                    new_visited = set(new_path)
                    score = -heuristic(new_pos, goal)
                    all_candidates.append((score, new_pos, new_path, new_visited))
                # Restart ngẫu nhiên nếu không thể backtrack
                else:
                    rand_r, rand_c = random.randint(0, R - 1), random.randint(0, C - 1)
                    while maze[rand_r][rand_c] == 1:
                        rand_r, rand_c = random.randint(0, R - 1), random.randint(0, C - 1)
                    new_pos = (rand_r, rand_c)
                    score = -heuristic(new_pos, goal)
                    all_candidates.append((score, new_pos, [new_pos], {new_pos}))
                continue

            # Tạo các ứng viên mới từ các hàng xóm
            for nbr in valid_neighbors:
                new_path = path + [nbr]
                new_visited = visited | {nbr}
                score = -heuristic(nbr, goal)
                all_candidates.append((score, nbr, new_path, new_visited))

        if not all_candidates:
            return None # Không còn ứng viên nào

        # Chọn top K ứng viên tốt nhất
        top_k = nlargest(k, all_candidates, key=lambda x: x[0])
        
        # Thêm một chút ngẫu nhiên để tránh bị kẹt cục bộ
        num_random = max(1, int(k * restart_rate))
        remaining = [c for c in all_candidates if c not in top_k]
        if remaining:
            random.shuffle(remaining)
            top_k.extend(remaining[:num_random])

        beams = [(pos, path, visited) for _, pos, path, visited in top_k]

    return None