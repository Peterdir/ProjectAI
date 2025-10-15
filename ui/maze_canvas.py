import tkinter as tk
from PIL import Image, ImageTk
from config import CELL_SIZE, PATH_COLOR, GRID_LINE_COLOR

class MazeCanvas(tk.Canvas):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height, bg="white")
        self.load_images()

    def load_images(self):
        self.wall_img = ImageTk.PhotoImage(Image.open("assets/wall.png").resize((CELL_SIZE, CELL_SIZE)))
        self.player_img = ImageTk.PhotoImage(Image.open("assets/player.png").resize((CELL_SIZE, CELL_SIZE)))
        self.goal_img = ImageTk.PhotoImage(Image.open("assets/goal.png").resize((CELL_SIZE, CELL_SIZE)))

    def draw_maze(self, maze, goal, show_grid):
        self.delete("all")
        rows, cols = len(maze), len(maze[0])

        for r in range(rows):
            for c in range(cols):
                x0, y0 = c * CELL_SIZE, r * CELL_SIZE
                if maze[r][c] == 1:
                    self.create_image(x0, y0, image=self.wall_img, anchor="nw")
                else:
                    x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                    self.create_rectangle(x0, y0, x1, y1, fill=PATH_COLOR, outline=PATH_COLOR)
        
        if show_grid:
            self.draw_grid_lines(rows, cols)

        gr, gc = goal
        self.create_image(gc * CELL_SIZE, gr * CELL_SIZE, image=self.goal_img, anchor="nw")

    def draw_player(self, player_pos):
        self.delete("player")
        r, c = player_pos
        self.create_image(c * CELL_SIZE, r * CELL_SIZE, image=self.player_img, anchor="nw", tags="player")

    def draw_grid_lines(self, rows, cols):
        self.delete("grid_line")
        for r in range(rows + 1):
            self.create_line(0, r * CELL_SIZE, cols * CELL_SIZE, r * CELL_SIZE, fill=GRID_LINE_COLOR, tag="grid_line")
        for c in range(cols + 1):
            self.create_line(c * CELL_SIZE, 0, c * CELL_SIZE, rows * CELL_SIZE, fill=GRID_LINE_COLOR, tag="grid_line")

    def highlight_cell(self, pos, color="yellow", start_pos=None, goal_pos=None):
        if pos == start_pos or pos == goal_pos:
            return
        r, c = pos
        x0, y0 = c * CELL_SIZE + 3, r * CELL_SIZE + 3
        x1, y1 = (c + 1) * CELL_SIZE - 3, (r + 1) * CELL_SIZE - 3
        self.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        self.update_idletasks() # Cập nhật ngay lập tức