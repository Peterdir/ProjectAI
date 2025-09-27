import heapq

def heuristic(node, goal):
    """Khoảng cách Manhattan:
    |x1 - x2| + |y1 - y2|"""
    x, y = node
    goalx, goaly = goal
    return abs(x - goalx) + abs(y - goaly)

def find_path(maze, start, goal, beam_width = 3):
    ROWS = len(maze)
    COLS = len(maze[0])
    start = (1,1)
    GOAL = (ROWS - 2, COLS -2)

    frontier = [(heuristic(start, goal), start, [start])]
    visited = set()

    while frontier:
        frontier = heapq.nsmallest(beam_width, frontier)

        new_frontier = []
        for score, (x,y), path in frontier:
            if(x,y) == goal:
                return path
            if(x, y) in visited:
                continue
            visited.add((x, y))
        
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] == 0:
                new_path = path +[(nx, ny)]
                new_score = heuristic((nx, ny), goal)
                new_frontier.append((new_score, (nx, ny), new_path))
        
        frontier = sorted(new_frontier, key = lambda x: x[0])

    return None
