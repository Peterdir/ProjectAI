# maze_solver/app.py
import tkinter as tk
from tkinter import messagebox
from config import *
from helpers.loader import load_algorithm
from core.maze_generator import generate_random_maze
from ui.maze_canvas import MazeCanvas
from ui.sidebar import Sidebar
from ui.controls_frame import ControlsFrame

class MazeApp:
    def __init__(self, root):
        self.root = root
        root.title("Mê Cung Solver (Refactored)")
        root.state("zoomed")

        # Khởi tạo trạng thái
        self.maze = MAZE
        self.player = START
        self.goal = GOAL
        self.solution = None
        self.running = False
        self.showing_solution = False
        self.algo_ran = False

        # Khởi tạo UI
        self.setup_ui()
        self.bind_events()

        # Vẽ lần đầu
        self.full_redraw()

    def setup_ui(self):
        # Frame chính
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE
        self.canvas = MazeCanvas(main_frame, width=canvas_w, height=canvas_h)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Controls
        control_callbacks = {
            "show_solution": self.show_solution,
            "reset": self.reset_app,
            "toggle_grid": self.toggle_grid_display,
            "random_maze": self.random_maze
        }
        self.controls = ControlsFrame(main_frame, control_callbacks)
        self.controls.grid(row=1, column=0, sticky="ew", pady=10)

        # Sidebar
        self.sidebar = Sidebar(main_frame, self.on_seed_double_click)
        self.sidebar.grid(row=0, column=1, rowspan=2, sticky="ns", padx=(10, 0))
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def bind_events(self):
        self.root.bind("<Up>", lambda e: self.move_player(-1, 0))
        self.root.bind("<Down>", lambda e: self.move_player(1, 0))
        self.root.bind("<Left>", lambda e: self.move_player(0, -1))
        self.root.bind("<Right>", lambda e: self.move_player(0, 1))
        # WASD keys
        self.root.bind("w", lambda e: self.move_player(-1, 0))
        self.root.bind("s", lambda e: self.move_player(1, 0))
        self.root.bind("a", lambda e: self.move_player(0, -1))
        self.root.bind("d", lambda e: self.move_player(0, 1))

    def full_redraw(self):
        show_grid = self.controls.toggle_grid_var.get()
        self.canvas.draw_maze(self.maze, self.goal, show_grid)
        self.canvas.draw_player(self.player)

    def move_player(self, dr, dc):
        if self.running or self.algo_ran: return
        
        nr, nc = self.player[0] + dr, self.player[1] + dc
        rows, cols = len(self.maze), len(self.maze[0])
        
        if 0 <= nr < rows and 0 <= nc < cols and self.maze[nr][nc] == 0:
            self.player = (nr, nc)
            self.canvas.draw_player(self.player)
            if self.player == self.goal:
                self.on_win()

    def on_win(self):
        messagebox.showinfo("Hoàn thành!", "Chúc mừng — bạn đã đến đích!")
    
    def show_solution(self):
        algo_name = self.controls.selected_algo.get()
        if not algo_name:
            messagebox.showwarning("Chưa có thuật toán", "Vui lòng chọn một thuật toán.")
            return

        if self.algo_ran:
            messagebox.showerror("Cảnh báo", "Vui lòng bấm Reset trước khi chạy thuật toán khác.")
            return

        if self.running:
            messagebox.showerror("Đang chạy", "Một thuật toán đang chạy — vui lòng đợi hoặc nhấn Reset.")
            return

        algorithm = load_algorithm(algo_name)
        self.running = True
        self.controls.set_controls_enabled(False)
        self.sidebar.update_metrics_table({})
        
        try:
            def update_callback(stats, **kwargs):
                if self.running:
                    highlight_keys = kwargs.get("highlight_keys", [])
                    self.sidebar.update_metrics_table(stats, highlight_keys)

            path, metrics = algorithm(
                self.maze, self.player, self.goal,
                callback=lambda pos: self.canvas.highlight_cell(pos, "blue", self.player, self.goal) if self.running else None,
                update_callback=update_callback
            )
            if not self.running: return

            self.sidebar.update_metrics_table(metrics)
            if not path:
                messagebox.showwarning("Không có đường", "Không tìm thấy đường đi.")
                self.reset_app() # Reset lại để người dùng thử lại
                return

            self.solution = path
            self.showing_solution = True
            self.algo_ran = True
            self.controls.lock_after_run()

            # Animate solution path
            for r, c in path:
                if not self.running: break
                self.canvas.highlight_cell((r, c), "green", self.player, self.goal)
                self.root.after(50)
                self.root.update()
            
            # Animate player movement
            for r, c in path:
                if not self.running: break
                self.player = (r, c)
                self.canvas.draw_player(self.player)
                self.root.after(100)
                self.root.update()

            if self.running:
                self.on_win()

        except Exception as e:
            messagebox.showerror("Lỗi thuật toán", f"Có lỗi xảy ra khi chạy thuật toán:\n{e}")
            import traceback
            print(traceback.format_exc())
        finally:
            self.running = False
            # Trạng thái controls đã được set bởi lock_after_run() nếu thành công
            # hoặc cần được bật lại nếu thất bại
            if not self.algo_ran:
                self.controls.set_controls_enabled(True)


    def reset_app(self):
        self.running = False # Dừng bất kỳ tiến trình nào đang chạy
        self.player = START
        self.solution = None
        self.showing_solution = False
        self.algo_ran = False
        self.controls.set_controls_enabled(True)
        self.sidebar.update_metrics_table({})
        self.full_redraw()

    def random_maze(self, seed=None):
        global ROWS, COLS, START, GOAL
        ROWS, COLS = 21, 31 # Có thể đưa ra config
        
        self.maze, self.player, self.goal, used_seed = generate_random_maze(ROWS, COLS, seed)
        START, GOAL = self.player, self.goal # Cập nhật global config nếu cần
        
        self.sidebar.add_seed_to_history(used_seed)
        self.reset_app() # Reset trạng thái ứng dụng với mê cung mới
        
        # Cập nhật lại kích thước canvas
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE
        self.canvas.config(width=canvas_w, height=canvas_h)
        self.full_redraw()

    def on_seed_double_click(self, event):
        if self.running:
            messagebox.showwarning("Đang chạy", "Vui lòng đợi thuật toán kết thúc.")
            return
        
        selection = self.sidebar.seed_listbox.curselection()
        if selection:
            seed = int(self.sidebar.seed_listbox.get(selection[0]))
            self.random_maze(seed)

    def toggle_grid_display(self):
        self.full_redraw()