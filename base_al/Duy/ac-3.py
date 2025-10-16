from collections import deque

def ac3_find_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    variables = [(r, c) for r in range(R) for c in range(C) if maze[r][c] == 0]

    domains = {v: [] for v in variables}
    for r, c in variables:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in variables:
                domains[(r, c)].append((nr, nc))

    queue = deque([(Xi, Xj) for Xi in variables for Xj in domains[Xi]])

    def revise(Xi, Xj):
        revised = False
        if Xj != goal and len(domains[Xj]) == 1:  
            if Xj in domains[Xi]:
                domains[Xi].remove(Xj)
                revised = True
        return revised

    while queue:
        Xi, Xj = queue.popleft()
        if revise(Xj, Xi):
            for Xk in domains[Xj]:
                if Xk != Xi:
                    queue.append((Xk, Xj))

    visited = set()

    def backtrack(state, path):
        if state == goal:
            return path + [state]
        visited.add(state)

        for next_state in domains.get(state, []):
            if next_state not in visited:
                result = backtrack(next_state, path + [state])
                if result:
                    return result
        return None

    path = backtrack(start, [])
    return path
