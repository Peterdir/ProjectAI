"""
maze_tkinter.py
Giao diện Tkinter cho mê cung có sẵn + nút hiện lời giải (BFS).
Chạy: python maze_tkinter.py
"""

import tkinter as tk
from collections import deque

# --- CẤU HÌNH ---
CELL_SIZE = 30
WALL_COLOR = "black"
PATH_COLOR = "white"
PLAYER_COLOR = "green"
GOAL_COLOR = "gold"
SOLUTION_COLOR = "skyblue"
GRID_LINE_COLOR = "#dddddd"


MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROWS = len(MAZE)
COLS = len(MAZE[0])

# Vị trí bắt đầu và đích (row, col)
START = (1, 1)
GOAL = (11, 13)

# --- HÀM TÌM ĐƯỜNG NGẮN NHẤT BẰNG BFS ---
def bfs_shortest_path(maze, start, goal):
    R, C = len(maze), len(maze[0])
    q = deque()
    q.append(start)
    prev = {start: None}
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    while q:
        r,c = q.popleft()
        if (r,c) == goal:
            break
        for dr,dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 0 and (nr,nc) not in prev:
                prev[(nr,nc)] = (r,c)
                q.append((nr,nc))
    if goal not in prev:
        return None
    # xây dựng đường đi
    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

# --- CLASS GIAO DIỆN ---
class MazeApp:
    def __init__(self, root):
        self.root = root
        root.title("Mê Cung - Tkinter (Có lời giải)")
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE

        self.canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Buttons
        self.show_btn = tk.Button(root, text="Show Solution", command=self.show_solution)
        self.show_btn.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.reset_btn = tk.Button(root, text="Reset", command=self.reset_player)
        self.reset_btn.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.toggle_grid_var = tk.BooleanVar(value=True)
        self.grid_btn = tk.Checkbutton(root, text="Grid lines", var=self.toggle_grid_var, command=self.draw_maze)
        self.grid_btn.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        # trạng thái
        self.player = START
        self.solution = None
        self.showing_solution = False

        # vẽ lần đầu
        self.draw_maze()
        self.draw_player()

        # bind phím mũi tên
        root.bind("<Up>", lambda e: self.move_player(-1,0))
        root.bind("<Down>", lambda e: self.move_player(1,0))
        root.bind("<Left>", lambda e: self.move_player(0,-1))
        root.bind("<Right>", lambda e: self.move_player(0,1))

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x0 = c * CELL_SIZE
                y0 = r * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                if MAZE[r][c] == 1:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=WALL_COLOR, outline=WALL_COLOR)
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=PATH_COLOR, outline=PATH_COLOR)
        # vẽ grid lines nếu bật
        if self.toggle_grid_var.get():
            for r in range(ROWS+1):
                self.canvas.create_line(0, r*CELL_SIZE, COLS*CELL_SIZE, r*CELL_SIZE, fill=GRID_LINE_COLOR)
            for c in range(COLS+1):
                self.canvas.create_line(c*CELL_SIZE, 0, c*CELL_SIZE, ROWS*CELL_SIZE, fill=GRID_LINE_COLOR)
        # vẽ đích
        gr, gc = GOAL
        self.canvas.create_rectangle(gc*CELL_SIZE, gr*CELL_SIZE, (gc+1)*CELL_SIZE, (gr+1)*CELL_SIZE,
                                     fill=GOAL_COLOR, outline="black")
        # nếu đã tính trước lời giải và đang hiển thị, vẽ nó
        if self.showing_solution and self.solution:
            for (r,c) in self.solution:
                x0 = c*CELL_SIZE + 3
                y0 = r*CELL_SIZE + 3
                x1 = (c+1)*CELL_SIZE - 3
                y1 = (r+1)*CELL_SIZE - 3
                self.canvas.create_rectangle(x0,y0,x1,y1, fill=SOLUTION_COLOR, outline="")
        # vẽ player sau cùng
        self.draw_player()

    def draw_player(self):
        # xóa layer player cũ
        self.canvas.delete("player")
        r,c = self.player
        x0 = c*CELL_SIZE + 4
        y0 = r*CELL_SIZE + 4
        x1 = (c+1)*CELL_SIZE - 4
        y1 = (r+1)*CELL_SIZE - 4
        self.canvas.create_oval(x0, y0, x1, y1, fill=PLAYER_COLOR, tags="player")

    def move_player(self, dr, dc):
        nr = self.player[0] + dr
        nc = self.player[1] + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            self.player = (nr, nc)
            self.draw_maze()
            # nếu chạm đích
            if self.player == GOAL:
                self.on_win()

    def on_win(self):
        # thông báo thắng
        tk.messagebox.showinfo("Hoàn thành!", "Chúc mừng — bạn đã đến đích!")
        # giữ nguyên trạng thái, user có thể reset hoặc xem lời giải

    def show_solution(self):
        # tính lời giải (BFS) và hiển thị
        path = bfs_shortest_path(MAZE, self.player, GOAL)
        if not path:
            tk.messagebox.showwarning("Không có đường", "Không tìm thấy đường từ vị trí hiện tại.")
            return
        self.solution = path
        self.showing_solution = True
        self.draw_maze()

    def reset_player(self):
        self.player = START
        self.solution = None
        self.showing_solution = False
        self.draw_maze()

# --- CHẠY APP ---
if __name__ == "__main__":
    # đảm bảo messagebox có sẵn
    import tkinter.messagebox
    root = tk.Tk()
    app = MazeApp(root)
    root.resizable(False, False)
    root.mainloop()
