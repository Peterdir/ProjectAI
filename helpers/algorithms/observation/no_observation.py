from collections import deque
import time

def find_path(maze, start, goal, callback=None, update_callback=None):
    """
    Improved sensorless (no observation) search algorithm using belief states.
    The search is performed using Breadth-First Search on the belief state space.
    """
    R, C = len(maze), len(maze[0])
    dirs = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    # --- SETUP BELIEF STATE SEARCH ---
    initial_belief_state = frozenset(
        (r, c) for r in range(R) for c in range(C) if maze[r][c] == 0
    )
    goal_belief_state = frozenset([goal])

    # Early exit if goal is not in the initial belief state
    if goal not in initial_belief_state:
        return None, {"Path found": False, "Reason": "Goal not reachable from initial belief state"}

    queue = deque([initial_belief_state])
    parent = {initial_belief_state: (None, None)}
    visited = {initial_belief_state}

    t0 = time.time()
    steps = 0
    solution_found = False

    # --- SEARCH LOOP ---
    while queue:
        current_b_state = queue.popleft()
        steps += 1

        if callback:
            callback(current_b_state)

        # Goal Test
        if current_b_state == goal_belief_state:
            solution_found = True
            break

        for action_name, (dr, dc) in dirs.items():
            next_b_state_set = set()
            for r, c in current_b_state:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0:
                    next_b_state_set.add((nr, nc))
                else:
                    next_b_state_set.add((r, c))

            next_b_state = frozenset(next_b_state_set)

            if next_b_state not in visited:
                visited.add(next_b_state)
                parent[next_b_state] = (current_b_state, action_name)
                queue.append(next_b_state)

        if update_callback:
            stats = {
                "Steps (Belief States)": steps,
                "Visited Belief States": len(visited),
                "Time (ms)": (time.time() - t0) * 1000,
                "Frontier Size": len(queue),
                "Current Belief State Size": len(current_b_state)
            }
            update_callback(stats, highlight_keys=stats.keys())

    # --- PATH RECONSTRUCTION ---
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

    path_length = len(path_of_actions)
    stats = {
        "Steps (Belief States)": steps,
        "Visited Belief States": len(visited),
        "Path Length (Actions)": path_length,
        "Time (ms)": (time.time() - t0) * 1000,
        "Path found": solution_found
    }

    return (final_path_coords, stats)