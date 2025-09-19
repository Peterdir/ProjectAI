import tkinter as tk
from config import *
from solver import bfs_shortest_path
from PIL import Image, ImageTk
#import messengerbox
from tkinter import messagebox
class MazeApp:
    def __init__(self, root):
        self.root = root
        root.title("Mê Cung - Tkinter (Có lời giải)")
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE

        self.canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.show_btn = tk.Button(root, text="Show Solution", command=self.show_solution)
        self.show_btn.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.reset_btn = tk.Button(root, text="Reset", command=self.reset_player)
        self.reset_btn.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.toggle_grid_var = tk.BooleanVar(value=True)
        self.grid_btn = tk.Checkbutton(root, text="Grid lines",
                                       var=self.toggle_grid_var, command=self.draw_maze)
        self.grid_btn.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        # Load images (resize theo CELL_SIZE luôn)
        self.wall_img = ImageTk.PhotoImage(Image.open("assets/wall.png").resize((CELL_SIZE, CELL_SIZE)))
        self.player_img = ImageTk.PhotoImage(Image.open("assets/player.png").resize((CELL_SIZE, CELL_SIZE)))
        self.goal_img = ImageTk.PhotoImage(Image.open("assets/goal.png").resize((CELL_SIZE, CELL_SIZE)))
        self.player = START
        self.solution = None
        self.showing_solution = False

        self.draw_maze()
        self.draw_player()

        root.bind("<Up>", lambda e: self.move_player(-1,0))
        root.bind("<Down>", lambda e: self.move_player(1,0))
        root.bind("<Left>", lambda e: self.move_player(0,-1))
        root.bind("<Right>", lambda e: self.move_player(0,1))

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x0, y0 = c*CELL_SIZE, r*CELL_SIZE
                x1, y1 = x0+CELL_SIZE, y0+CELL_SIZE
                if MAZE[r][c] == 1:
                    self.canvas.create_image(x0, y0, image=self.wall_img, anchor="nw")
                else:
                    self.canvas.create_rectangle(x0,y0,x1,y1, fill=PATH_COLOR, outline=PATH_COLOR)

        if self.toggle_grid_var.get():
            for r in range(ROWS+1):
                self.canvas.create_line(0, r*CELL_SIZE, COLS*CELL_SIZE, r*CELL_SIZE, fill=GRID_LINE_COLOR)
            for c in range(COLS+1):
                self.canvas.create_line(c*CELL_SIZE, 0, c*CELL_SIZE, ROWS*CELL_SIZE, fill=GRID_LINE_COLOR)

        gr, gc = GOAL
        self.canvas.create_image(gc*CELL_SIZE, gr*CELL_SIZE, image=self.goal_img, anchor="nw")

        if self.showing_solution and self.solution:
            for (r,c) in self.solution:
                x0, y0 = c*CELL_SIZE+3, r*CELL_SIZE+3
                x1, y1 = (c+1)*CELL_SIZE-3, (r+1)*CELL_SIZE-3
                self.canvas.create_rectangle(x0,y0,x1,y1, fill=SOLUTION_COLOR, outline="")

        self.draw_player()

    def draw_player(self):
        self.canvas.delete("player")
        r, c = self.player
        self.canvas.create_image(c*CELL_SIZE, r*CELL_SIZE, image=self.player_img, anchor="nw", tags="player")

    def move_player(self, dr, dc):
        nr, nc = self.player[0]+dr, self.player[1]+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            self.player = (nr, nc)
            self.draw_maze()
            if self.player == GOAL:
                self.on_win()

    def on_win(self):
        tk.messagebox.showinfo("Hoàn thành!", "Chúc mừng — bạn đã đến đích!")

    def show_solution(self):
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
