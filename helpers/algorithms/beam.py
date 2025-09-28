import heapq

def heuristic(node, goal):
    """Khoảng cách Manhattan: |x1 - x2| + |y1 - y2|"""
    x, y = node
    gx, gy = goal
    return abs(x - gx) + abs(y - gy)

def find_path(maze, start, goal, callback = None, beam_width=3):
    """
    Beam Search đơn giản.
    - Không ghi đè start/goal (dùng giá trị được truyền vào).
    - Mỗi phần tử frontier: (score, (r,c), path)
    """
    ROWS, COLS = len(maze), len(maze[0])

    # Khởi tạo frontier bằng đúng start được truyền vào
    frontier = [(heuristic(start, goal), start, [start])]
    visited = set()

    while frontier:
        # Giữ lại beam_width ứng viên tốt nhất (theo score nhỏ)
        frontier = heapq.nsmallest(beam_width, frontier)

        new_frontier = []
        for score, (x, y), path in frontier:
            # Nếu đến goal thì trả về path từ start -> goal
            if (x, y) == goal:
                return path

            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                    if (nx, ny) in visited:
                        continue
                    new_path = path + [(nx, ny)]
                    new_score = heuristic((nx, ny), goal)
                    new_frontier.append((new_score, (nx, ny), new_path))

                    # Gọi callback để tô màu ô đang xét
                    if callback:
                        callback((nx, ny))

        # Sắp xếp các ứng viên mới theo score (nhỏ->lớn) và dùng ở vòng tiếp theo
        frontier = sorted(new_frontier, key=lambda x: x[0])

    return None
