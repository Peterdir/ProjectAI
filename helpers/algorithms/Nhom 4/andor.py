import time

MAX_DEPTH = 200

def find_path(maze, start, goal, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    steps = 0
    visited = set()
    t0 = time.time()
    stats = {}

    def check_valid(r, c):
        return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

    def result(state, action):
        dr, dc = action
        nr, nc = state[0] + dr, state[1] + dc
        if check_valid(nr, nc):
            return [(nr, nc)]  # 1 trạng thái kết quả duy nhất
        return []  # không hợp lệ

    def or_search(state, path):
        nonlocal steps, stats
        steps += 1

        stats.update({
            "Steps": steps,
            "Visited nodes": len(visited),
            "Current node": state,
            "Path length": len(path),
            "Time (ms)": (time.time() - t0) * 1000
        })
        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))
        if callback:
            callback(state)

        if len(path) > MAX_DEPTH:
            return None
        if state == goal:
            return []  # Kế hoạch rỗng → đã đạt mục tiêu
        if state in path:
            return None  # tránh lặp

        visited.add(state)

        for action in actions:
            result_states = result(state, action)
            if not result_states:
                continue

            plan = and_search(result_states, path + [state])
            if plan is not None:
                return [action, plan]

        return None

    def and_search(states, path):
        plans = []
        for s in states:
            plan = or_search(s, path)
            if plan is None:
                return None  # Nếu 1 nhánh thất bại, toàn bộ thất bại
            plans.append(plan)
        return plans

    solution_plan = or_search(start, [])

    def extract_path_from_plan(plan, current_state):
        path = [current_state]
        if isinstance(plan, list) and len(plan) == 2:
            (dr, dc), subplan = plan
            next_state = (current_state[0] + dr, current_state[1] + dc)
            path += extract_path_from_plan(subplan, next_state)
        elif isinstance(plan, list) and all(isinstance(p, list) for p in plan):
            for sub in plan:
                path += extract_path_from_plan(sub, current_state)
        return path

    path = extract_path_from_plan(solution_plan, start) if solution_plan else []

    stats.update({
        "Steps": steps,
        "Visited nodes": len(visited),
        "Path length": len(path),
        "Found": bool(path),
        "Time (ms)": (time.time() - t0) * 1000
    })
    if update_callback:
        update_callback(stats, highlight_keys=list(stats.keys()))

    return path, stats
