import heapq
def cost():
    return 1
def find_path(maze, start, goal):
    ROWS = len(maze)
    COLS = len(maze[0])

    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, (x,y), path = heapq.pop()

        if (x,y) == goal:
            return path, cost
        
        if (x,y) in visited:
            continue
        visited.add((x,y))

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[0][0]:
                if (nx,ny) not in visited:
                    heapq.heappush(pq,(cost + 1, (nx,ny), path + [(nx,ny)]))
                
        
        return None, None # Bó tay