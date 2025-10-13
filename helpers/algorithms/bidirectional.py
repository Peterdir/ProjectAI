from collections import deque
import time

def find_path(maze, start, goal, callback=None, update_callback=None):
    """
    Bidirectional BFS search algorithm implementation (Corrected & Optimized).
    """
    R, C = len(maze), len(maze[0])
    
    # --- SETUP ---
    # Hàng đợi cho cả hai hướng
    queue_start = deque([start])
    queue_goal = deque([goal])
    
    # Dùng parent dict để theo dõi các nút đã thăm và đường đi
    # Không cần các biến visited_* riêng biệt nữa
    parent_start = {start: None}
    parent_goal = {goal: None}
    
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    steps = 0
    intersection = None
    t0 = time.time()
    
    # --- SEARCH LOOP ---
    while queue_start and queue_goal:
        
        # TỐI ƯU: Luôn mở rộng từ hàng đợi (frontier) nhỏ hơn trước
        if len(queue_start) <= len(queue_goal):
            # Mở rộng từ `start`
            current = queue_start.popleft()
            
            # SỬA LỖI: Kiểm tra giao nhau với parent dict của hướng ngược lại
            if current in parent_goal:
                intersection = current
                break
                
            # Mở rộng các nút lân cận
            for dr, dc in dirs:
                nr, nc = current[0] + dr, current[1] + dc
                if (0 <= nr < R and 0 <= nc < C and 
                    maze[nr][nc] == 0 and 
                    (nr, nc) not in parent_start):
                    parent_start[(nr, nc)] = current
                    queue_start.append((nr, nc))
        else:
            # Mở rộng từ `goal`
            current = queue_goal.popleft()

            # SỬA LỖI: Kiểm tra giao nhau với parent dict của hướng ngược lại
            if current in parent_start:
                intersection = current
                break

            # Mở rộng các nút lân cận
            for dr, dc in dirs:
                nr, nc = current[0] + dr, current[1] + dc
                if (0 <= nr < R and 0 <= nc < C and
                    maze[nr][nc] == 0 and
                    (nr, nc) not in parent_goal):
                    parent_goal[(nr, nc)] = current
                    queue_goal.append((nr, nc))

        steps += 1
        if callback:
            callback(current)
        if update_callback:
            stats = {
                "Steps": steps,
                "Visited nodes": len(parent_start) + len(parent_goal),
                "Time (ms)": (time.time() - t0) * 1000,
                "Frontier size": len(queue_start) + len(queue_goal)
            }
            update_callback(stats, highlight_keys=["Steps", "Visited nodes", "Time (ms)", "Frontier size"])

    # --- PATH RECONSTRUCTION ---
    path = None
    if intersection:
        path = []
        # Đi ngược từ điểm giao nhau về `start`
        node = intersection
        while node:
            path.append(node)
            node = parent_start.get(node)
        path.reverse()
        
        # Đi ngược từ điểm giao nhau về `goal` và nối vào
        node = parent_goal.get(intersection)
        while node:
            path.append(node)
            node = parent_goal.get(node)
            
    # --- FINAL STATS ---
    path_length = len(path) if path else 0
    stats = {
        "Steps": steps,
        "Visited nodes": len(parent_start) + len(parent_goal),
        "Path length": path_length,
        "Time (ms)": (time.time() - t0) * 1000,
        "Path found": intersection is not None
    }
    
    return (path, stats) if intersection else (None, stats)