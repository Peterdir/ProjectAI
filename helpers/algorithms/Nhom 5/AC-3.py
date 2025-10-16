import time
from collections import deque

MAX_DEPTH = 500 # Tăng giới hạn độ sâu cho các mê cung lớn

def find_path(maze, start, goal, callback=None, update_callback=None):
    R, C = len(maze), len(maze[0])
    
    stats = {
        "Steps": 0, "Visited nodes": 0, "Path length": 0, "Time (ms)": 0.0,
        "Pruned Nodes": 0
    }
    t0 = time.time()
    
    variables = [(r, c) for r in range(R) for c in range(C) if maze[r][c] == 0]
    
    domains = {v: [] for v in variables}
    for r, c in variables:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in variables:
                domains[(r, c)].append((nr, nc))

    initial_domain_size = sum(len(d) for d in domains.values())

    queue = deque([(Xi, Xj) for Xi in variables for Xj in domains[Xi]])

    def revise(Xi, Xj):
        revised = False
        if Xj != goal and len(domains[Xj]) == 1: # Xj chỉ có 1 lối ra duy nhất là quay lại Xi
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

    final_domain_size = sum(len(d) for d in domains.values())
    stats["Pruned Nodes"] = (initial_domain_size - final_domain_size) // 2


    visited = set()
    
    def back_trackSearch(state, path):
        nonlocal stats
        stats["Steps"] += 1
        stats["Visited nodes"] = len(visited)
        stats["Path length"] = len(path)
        stats["Time (ms)"] = (time.time() - t0) * 1000

        if update_callback: update_callback(stats, highlight_keys=list(stats.keys()))
        if callback: callback(state)

        if len(path) > MAX_DEPTH: return None
        if state == goal: return []
        if state in path: return None

        visited.add(state)

        for next_state in domains.get(state, []):
            plan = back_trackSearch(next_state, path + [state])
            if plan is not None:
                return [next_state] + plan
        
        return None

    solution_path_nodes = back_trackSearch(start, [])
    
    path = []
    if solution_path_nodes is not None:
        path = [start] + solution_path_nodes

    stats["Path length"] = len(path)
    stats["Visited nodes"] = len(visited)
    stats["Time (ms)"] = (time.time() - t0) * 1000

    if update_callback: update_callback(stats, highlight_keys=list(stats.keys()))
    return path, stats