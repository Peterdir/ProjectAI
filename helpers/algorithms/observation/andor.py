import time

MAX_DEPTH = 200

def find_path(maze, start, goal, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    actions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    stats = {
        "Steps": 0,
        "Visited nodes": 0,
        "Path length": 0,
        "Time (ms)": 0.0
    }
    visited = set()
    t0 = time.time()

    def check_valid(r, c):
        return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

    def result(state, action):
        dr, dc = action
        nr, nc = state[0] + dr, state[1] + dc
        if check_valid(nr, nc):
            return [(nr, nc)]
        return []

    # ==========================
    #  HÀM OR_SEARCH (chọn hành động)
    # ==========================
    def or_search(state, path):
        nonlocal stats

        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))
        if callback:
            callback(state)

        # --- Điều kiện dừng ---
        if len(path) > MAX_DEPTH:
            return None
        if state == goal:
            return []
        if state in path:
            return None

        visited.add(state)

        # --- Duyệt từng hành động ---
        for dr, dc in actions:
            result_states = result(state, (dr, dc))
            if not result_states:
                continue

            # Gọi hàm and_search cho tất cả kết quả hành động
            plan = and_search(result_states, path + [state])
            if plan is not None:
                return [(dr, dc), plan]

        return None

    def and_search(states, path):
        plans = []
        for s in states:
            plan = or_search(s, path)
            if plan is None:
                return None  # Nếu một trạng thái thất bại → hành động thất bại
            plans.append(plan)
        return plans

    def extract_path_from_plan(plan, current_state):
        path = [current_state]
        if isinstance(plan, list) and len(plan) == 2:
            (dr, dc), subplan = plan
            if subplan is not None:
                next_state = (current_state[0] + dr, current_state[1] + dc)
                path += extract_path_from_plan(subplan, next_state)
        elif isinstance(plan, list) and all(isinstance(p, list) for p in plan):
            for sub in plan:
                path += extract_path_from_plan(sub, current_state)
        return path

    solution_plan = or_search(start, [])
    path = extract_path_from_plan(solution_plan, start) if solution_plan else []

    stats["Path length"] = len(path)
    stats["Visited nodes"] = len(visited)
    stats["Time (ms)"] = (time.time() - t0) * 1000

    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))

    return path, stats
