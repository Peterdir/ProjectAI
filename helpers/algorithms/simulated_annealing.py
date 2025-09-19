import random
import math

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def find_path(maze, start, goal, max_steps=100000, initial_temp=100.0, cooling_rate=0.995):
    R, C = len(maze), len(maze[0])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    path = [start]
    current = start
    steps = 0
    temp = initial_temp
    visited = set([start])
    deadend_counter = 0

    while current != goal and steps < max_steps:
        steps += 1
        r, c = current
        neighbors = [(r+dr, c+dc) for dr, dc in dirs if 0<=r+dr<R and 0<=c+dc<C and maze[r+dr][c+dc]==0 and (r+dr,c+dc) not in visited]

        if not neighbors:
            deadend_counter += 1
            if len(path) > 1:
                # lùi tới ô gần nhất có neighbor chưa thử
                for i in range(len(path)-2, -1, -1):
                    r2, c2 = path[i]
                    new_neighbors = [(r2+dr,c2+dc) for dr, dc in dirs if 0<=r2+dr<R and 0<=c2+dc<C and maze[r2+dr][c2+dc]==0 and (r2+dr,c2+dc) not in visited]
                    if new_neighbors:
                        current = (r2,c2)
                        path = path[:i+1]
                        break
            else:
                return None
            # restart nếu deadend lâu quá
            if deadend_counter > 50:
                current = random.choice(path)
                temp = initial_temp
                deadend_counter = 0
            continue

        deadend_counter = 0
        next_cell = random.choice(neighbors)
        delta_h = heuristic(next_cell, goal) - heuristic(current, goal)
        if delta_h < 0 or random.random() < math.exp(-delta_h/temp):
            current = next_cell
            path.append(current)
            visited.add(current)
        temp *= cooling_rate
        if temp < 1e-3:
            temp = initial_temp

    return path if current==goal else None
