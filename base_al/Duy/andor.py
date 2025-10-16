MAX_DEPTH = 200

def and_or_find_path(maze, start, goal):

    R, C = len(maze), len(maze[0])
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()

    def check_valid(r, c):
        return 0 <= r < R and 0 <= c < C and maze[r][c] == 0

    def result(state, action):
        dr, dc = action
        nr, nc = state[0] + dr, state[1] + dc
        if check_valid(nr, nc):
            return [(nr, nc)]
        return []

    def or_search(state, path):
        if state == goal:
            return []  # đạt mục tiêu
        if state in path or len(path) > MAX_DEPTH:
            return None  # tránh vòng lặp hoặc quá sâu

        visited.add(state)

        for action in actions:
            result_states = result(state, action)
            if not result_states:
                continue

            plan = and_search(result_states, path + [state])
            if plan is not None:
                return [action, plan]  # thành công với hành động này

        return None  # thất bại ở mọi hành động

    def and_search(states, path):
        plans = []
        for s in states:
            plan = or_search(s, path)
            if plan is None:
                return None  # một nhánh thất bại → toàn bộ thất bại
            plans.append(plan)
        return plans

    return or_search(start, [])
