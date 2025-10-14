from collections import deque
import time
import random

def find_path(maze, start, goal, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    dirs = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    initial_belief_state = frozenset(
        (r, c) for r in range(R) for c in range(C) if maze[r][c] == 0
    )
    goal_belief_state = frozenset([goal])

    if goal not in initial_belief_state:
        return None, {"Path found": False, "Reason": "Goal not reachable"}

    queue = deque([initial_belief_state])
    parent = {initial_belief_state: (None, None)}
    visited = {initial_belief_state}
    dead_ends = set()

    t0 = time.time()
    steps = 0
    solution_found = False

    while queue:
        current_b_state = queue.popleft()
        steps += 1

        # 🔹 Chỉ highlight một ô duy nhất để tránh lỗi unpack
        if callback:
            sample_pos = random.choice(tuple(current_b_state))
            callback(sample_pos)

        if current_b_state == goal_belief_state:
            solution_found = True
            break

        next_states = []
        for action_name, (dr, dc) in dirs.items():
            next_b_state_set = set()
            for r, c in current_b_state:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
                    next_b_state_set.add((nr, nc))
                else:
                    next_b_state_set.add((r, c))

            next_b_state = frozenset(next_b_state_set)
            next_states.append((action_name, next_b_state))

        # Dead-end check
        if all(ns == current_b_state for _, ns in next_states):
            dead_ends.add(current_b_state)
            continue

        for action_name, next_b_state in next_states:
            if next_b_state not in visited and next_b_state not in dead_ends:
                visited.add(next_b_state)
                parent[next_b_state] = (current_b_state, action_name)
                queue.append(next_b_state)

        if update_callback:
            stats = {
                "Steps (Belief States)": steps,
                "Visited": len(visited),
                "Dead Ends": len(dead_ends),
                "Frontier": len(queue),
                "Time (ms)": (time.time() - t0) * 1000
            }
            update_callback(stats, highlight_keys=stats.keys())

    path_of_actions = []
    final_path_coords = None

    if solution_found:
        curr = goal_belief_state
        while curr != initial_belief_state:
            prev, action = parent[curr]
            path_of_actions.append(action)
            curr = prev
        path_of_actions.reverse()

        final_path_coords = [start]
        r, c = start
        for action_name in path_of_actions:
            dr, dc = dirs[action_name]
            r, c = r + dr, c + dc
            final_path_coords.append((r, c))

    stats = {
        "Steps (Belief States)": steps,
        "Visited": len(visited),
        "Dead Ends": len(dead_ends),
        "Path Length": len(path_of_actions),
        "Time (ms)": (time.time() - t0) * 1000,
        "Path found": solution_found
    }

    return (final_path_coords, stats)
