import tkinter as tk
from config import *
from helpers.loader import load_algorithm
from PIL import Image, ImageTk
from tkinter import messagebox,ttk
import os
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

        # Load danh sách thuật toán từ thư mục
        algo_dir = "helpers/algorithms"
        self.algorithms = [f[:-3] for f in os.listdir(algo_dir) 
                           if f.endswith(".py") and f != "__init__.py"] # Lệnh dùng để lấy tên các thuật toán có trong helpers/algorithms
        self.selected_algo = tk.StringVar(value=self.algorithms[0] if self.algorithms else "") # Nếu self.algorithms không rỗng lưu thuật đầu tiên
        self.algo_menu = tk.OptionMenu(root, self.selected_algo, *self.algorithms) # Tạo 1 dropdown menu 
        self.algo_menu.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        
        self.right_panel = tk.Frame(root)
        self.right_panel.grid(row=0, column=3, rowspan=2, sticky="ns", padx=(5, 5), pady=5)
                # Dropdown chọn thuật toán đặt ở trên cùng panel phải
        self.algo_menu = tk.OptionMenu(self.right_panel, self.selected_algo, *self.algorithms)
        self.algo_menu.pack(side="top", fill="x", pady=(0,5))

        # Bảng hiển thị chỉ số thuật toán (dạng key-value để hỗ trợ nhiều thuật toán)
        self.metrics_tree = ttk.Treeview(
            self.right_panel,
            columns=("metric", "value"),
            show="headings",
            height=15,
        )
        self.metrics_tree.heading("metric", text="Chỉ số")
        self.metrics_tree.heading("value", text="Giá trị")
        self.metrics_tree.column("metric", width=160, anchor="w")
        self.metrics_tree.column("value", width=180, anchor="center")

        # Scrollbar dọc cho bảng
        metrics_scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=self.metrics_tree.yview)
        self.metrics_tree.configure(yscrollcommand=metrics_scrollbar.set)

        # Sắp xếp trong khung bên phải
        self.metrics_tree.pack(side="left", fill="both", expand=True)
        metrics_scrollbar.pack(side="right", fill="y")
        # Load images (resize theo CELL_SIZE luôn)
        self.wall_img = ImageTk.PhotoImage(Image.open("assets/wall.png").resize((CELL_SIZE, CELL_SIZE)))
        self.player_img = ImageTk.PhotoImage(Image.open("assets/player.png").resize((CELL_SIZE, CELL_SIZE)))
        self.goal_img = ImageTk.PhotoImage(Image.open("assets/goal.png").resize((CELL_SIZE, CELL_SIZE)))
        self.player = START
        self.solution = None
        self.running = False
        self.showing_solution = False

        self.draw_maze()
        self.draw_player()

        root.bind("<Up>", lambda e: self.move_player(-1,0))
        root.bind("<Down>", lambda e: self.move_player(1,0))
        root.bind("<Left>", lambda e: self.move_player(0,-1))
        root.bind("<Right>", lambda e: self.move_player(0,1))
        # Thêm WASD
        root.bind("w", lambda e: self.move_player(-1,0))
        root.bind("s", lambda e: self.move_player(1,0))
        root.bind("a", lambda e: self.move_player(0,-1))
        root.bind("d", lambda e: self.move_player(0,1))
        
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
                if (r, c) == GOAL or (r, c) == START:
                    continue
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
        algo_name = self.selected_algo.get()

        if not algo_name:
            tk.messagebox.showwarning("Chưa có thuật toán", "Không tìm thấy thuật toán nào trong thư mục.")
            return
        
        algorithm = load_algorithm(algo_name)
        self.running = True
        
        # Chức năng mới (Tô màu các ô được mở rộng đề tìm kiếm)
        def callback(pos):
            if not self.running:
                return
            self.highlight_cell(pos, color="blue")

        path = algorithm(MAZE, self.player, GOAL, callback=callback)
        
        if not self.running:
            return
        if not path:
            tk.messagebox.showwarning("Không có đường", "Không tìm thấy đường từ vị trí hiện tại.")
            return
        
        self.solution = path
        self.showing_solution = True

        for r, c in path:
            if not self.running:
                break
            self.highlight_cell((r, c), color="green")
            self.canvas.update()
            self.canvas.after(50)

        for r, c in path:
            if not self.running:
                break
            self.player = (r, c)
            self.draw_player()
            self.canvas.update()
            self.canvas.after(100)

        if self.running:
            self.on_win()
        self.running = False

    def reset_player(self):
        self.running = False
        self.player = START
        self.solution = None
        self.showing_solution = False
        self.draw_maze()

    # Chức năng mới (Tô màu các ô được mở rộng để tìm kiếm)
    def highlight_cell(self, pos, color="yellow"):
        r, c = pos
        if (r, c) == START or (r, c) == GOAL:
            return

        x0, y0 = c*CELL_SIZE+3, r*CELL_SIZE+3
        x1, y1 = (c+1)*CELL_SIZE-3, (r+1)*CELL_SIZE-3
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        self.canvas.update()
        self.canvas.after(1)   
    
    def update_metrics_table(self, metrics):
        # Xóa dòng cũ
        for item in self.metrics_tree.get_children():
            self.metrics_tree.delete(item)

        if not metrics:
            return

        # Chèn từng cặp key-value. Định dạng các giá trị số cho đẹp.
        for key, val in metrics.items():
            display_val = val
            if isinstance(val, float):
                # Định dạng ms/ratio đẹp hơn
                if key.endswith("ms"):
                    display_val = f"{val:.3f}"
                else:
                    display_val = f"{val:.4f}"
            self.metrics_tree.insert("", "end", values=(key, display_val))
    