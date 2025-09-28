import random
import time

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def generate_individual(start, length=100):
    moves = ['U','D','L','R']
    return [random.choice(moves) for _ in range(length)]

def move_pos(pos, move):
    r,c = pos
    if move=='U': return (r-1, c)
    if move=='D': return (r+1, c)
    if move=='L': return (r, c-1)
    if move=='R': return (r, c+1)
    return pos

def fitness(maze, start, goal, individual):
    pos = start
    visited = set([start])
    for move in individual:
        r,c = move_pos(pos, move)
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c]==0:
            pos = (r,c)
            visited.add(pos)
        else:
            break
    dist = heuristic(pos, goal)
    return -dist + len(visited)*0.01

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1)-1)
    return parent1[:point]+parent2[point:], parent2[:point]+parent1[point:]

def mutate(individual, mutation_rate=0.1):
    moves = ['U','D','L','R']
    return [random.choice(moves) if random.random()<mutation_rate else m for m in individual]

def find_path(maze, start, goal, callback=None, update_callback=None,
              population_size=50, generations=200, move_length=150):
    population = [generate_individual(start, move_length) for _ in range(population_size)]
    t0 = time.time()
    steps = 0
    stats = {}

    for gen in range(generations):
        steps += 1
        scored = [(fitness(maze, start, goal, ind), ind) for ind in population]
        scored.sort(reverse=True, key=lambda x:x[0])

        best_fit, best_ind = scored[0]
        pos = start
        path = [start]

        for move in best_ind:
            r,c = move_pos(pos, move)
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c]==0:
                pos = (r,c)
                path.append(pos)
                if callback:
                    callback(pos)
            if pos == goal:
                # stats cuối cùng
                stats = {
                    "Steps": steps,
                    "Generation": gen+1,
                    "Visited nodes": len(set(path)),
                    "Path length": len(path),
                    "Time (ms)": (time.time()-t0)*1000
                }
                if update_callback:
                    update_callback(stats, highlight_keys=list(stats.keys()))
                return path, stats

        # stats realtime mỗi generation
        stats = {
            "Steps": steps,
            "Generation": gen+1,
            "Best fitness": best_fit,
            "Visited nodes": len(set(path)),
            "Path length": len(path),
            "Time (ms)": (time.time()-t0)*1000
        }
        if update_callback:
            update_callback(stats, highlight_keys=list(stats.keys()))

        # chọn top 20% làm parent
        num_parents = max(2, population_size//5)
        parents = [ind for _, ind in scored[:num_parents]]

        new_population = []
        while len(new_population) < population_size:
            p1, p2 = random.sample(parents, 2)
            c1, c2 = crossover(p1, p2)
            new_population.append(mutate(c1))
            if len(new_population) < population_size:
                new_population.append(mutate(c2))
        population = new_population

    return None, stats
