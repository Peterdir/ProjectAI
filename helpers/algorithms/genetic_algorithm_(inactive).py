import random

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def generate_individual(start, length=100):
    """Tạo một cá thể: chuỗi move ngẫu nhiên"""
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
        # nếu dead-end thì dừng cá thể tại đây
        else:
            break
    # fitness cao nếu gần goal, cộng thêm reward cho số ô đi được
    dist = heuristic(pos, goal)
    return -dist + len(visited)*0.01  # kết hợp gần goal + khám phá

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1)-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual, mutation_rate=0.1):
    moves = ['U','D','L','R']
    return [random.choice(moves) if random.random() < mutation_rate else m for m in individual]

def find_path(maze, start, goal, callback = None, population_size=50, generations=200, move_length=150):
    # khởi tạo population
    population = [generate_individual(start, move_length) for _ in range(population_size)]
    
    for gen in range(generations):
        # tính fitness
        scored = [(fitness(maze, start, goal, ind), ind) for ind in population]
        scored.sort(reverse=True, key=lambda x:x[0])

        # nếu cá thể nào đến goal, xây path thật
        best_fit, best_ind = scored[0]
        pos = start
        path = [start]
        for move in best_ind:
            r,c = move_pos(pos, move)
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c]==0:
                pos = (r,c)
                path.append(pos)

                if callback:
                    callback(pos)  # tô màu ô này
            if pos==goal:
                return path

        # chọn top 20% làm parent
        num_parents = max(2, population_size // 5)
        parents = [ind for _,ind in scored[:num_parents]]

        # sinh offspring bằng crossover
        new_population = []
        while len(new_population) < population_size:
            p1, p2 = random.sample(parents, 2)
            c1, c2 = crossover(p1,p2)
            new_population.append(mutate(c1))
            if len(new_population) < population_size:
                new_population.append(mutate(c2))
        population = new_population

    # nếu không tìm được goal
    return None
