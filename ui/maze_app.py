import customtkinter as ctk
from config import *
from helpers.loader import load_algorithm
from core.maze_generator import generate_random_maze
from ui.maze_canvas import MazeCanvas
from ui.sidebar import Sidebar
from ui.controls_frame import ControlsFrame
from ui.random_walls_toggle import RandomWallsToggle
from ui.start_position_input import ask_start_position
import random
import traceback
from CTkMessagebox import CTkMessagebox


class MazeApp:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("Mê Cung Solver (CTk Edition)")
        self.root.state("zoomed")

        # Trạng thái
        self.maze = MAZE
        self.player = START
        self.goal = GOAL
        self.solution = None
        self.running = False
        self.showing_solution = False
        self.algo_ran = False

        # Giao diện
        self.setup_ui()
        self.bind_events()
        self.full_redraw()

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Canvas
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE
        self.canvas = MazeCanvas(main_frame, width=canvas_w, height=canvas_h)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Nút chọn vị trí bắt đầu
        set_start_btn = ctk.CTkButton(
            main_frame, text="Đặt vị trí bắt đầu", command=self.set_custom_start
        )
        set_start_btn.grid(row=2, column=0, sticky="e", pady=(10, 0))

        # Controls
        control_callbacks = {
            "show_solution": self.show_solution,
            "reset": self.reset_app,
            "toggle_grid": self.toggle_grid_display,
            "random_maze": self.random_maze,
            "change_size": self.change_maze_size,
        }
        self.controls = ControlsFrame(main_frame, control_callbacks)
        self.controls.grid(row=1, column=0, sticky="ew", pady=10)

        # Sidebar
        self.sidebar = Sidebar(main_frame, self.on_seed_double_click)
        self.sidebar.grid(row=0, column=1, rowspan=2, sticky="ns", padx=(10, 0))

        # Toggle thêm tường ngẫu nhiên
        self.random_walls_toggle = RandomWallsToggle(
            main_frame, callback=lambda state: print("Random walls:", state)
        )
        self.random_walls_toggle.grid(row=2, column=0, sticky="w", pady=(10, 0))

    def bind_events(self):
        # CustomTkinter vẫn hỗ trợ bind như Tkinter
        self.root.bind("<Up>", lambda e: self.move_player(-1, 0))
        self.root.bind("<Down>", lambda e: self.move_player(1, 0))
        self.root.bind("<Left>", lambda e: self.move_player(0, -1))
        self.root.bind("<Right>", lambda e: self.move_player(0, 1))
        self.root.bind("w", lambda e: self.move_player(-1, 0))
        self.root.bind("s", lambda e: self.move_player(1, 0))
        self.root.bind("a", lambda e: self.move_player(0, -1))
        self.root.bind("d", lambda e: self.move_player(0, 1))
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def full_redraw(self):
        show_grid = self.controls.toggle_grid_var.get()
        self.canvas.draw_maze(self.maze, self.goal, show_grid)
        self.canvas.draw_player(self.player)

    def move_player(self, dr, dc):
        if self.running or self.algo_ran:
            return
        nr, nc = self.player[0] + dr, self.player[1] + dc
        rows, cols = len(self.maze), len(self.maze[0])

        if 0 <= nr < rows and 0 <= nc < cols and self.maze[nr][nc] == 0:
            self.player = (nr, nc)
            self.canvas.draw_player(self.player)

            if self.random_walls_toggle.is_enabled():
                self.add_random_walls(count=3)
                self.full_redraw()

            if self.player == self.goal:
                self.on_win()

    def add_random_walls(self, count=3):
        rows, cols = len(self.maze), len(self.maze[0])
        added = 0
        while added < count:
            r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if self.maze[r][c] == 0 and (r, c) not in [self.player, self.goal]:
                self.maze[r][c] = 1
                added += 1

    def on_win(self):
        CTkMessagebox(title="Hoàn thành!", message="Chúc mừng — bạn đã đến đích!")

    def show_solution(self):
        algo_name = self.controls.get_selected_algorithm_key()
        if not algo_name:
            CTkMessagebox(
                title="Chưa có thuật toán",
                message="Vui lòng chọn một thuật toán.",
                icon="warning",
            )
            return

        if self.algo_ran:
            CTkMessagebox(
                title="Cảnh báo",
                message="Vui lòng bấm Reset trước khi chạy thuật toán khác.",
                icon="cancel",
            )
            return

        if self.running:
            CTkMessagebox(
                title="Đang chạy",
                message="Một thuật toán đang chạy — vui lòng đợi hoặc nhấn Reset.",
                icon="info",
            )
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
                self.maze,
                self.player,
                self.goal,
                callback=lambda pos: self.canvas.highlight_cell(
                    pos, "blue", self.player, self.goal
                )
                if self.running
                else None,
                update_callback=update_callback,
            )
            if not self.running:
                return

            self.sidebar.update_metrics_table(metrics)
            if not path:
                CTkMessagebox(
                    title="Không có đường",
                    message="Không tìm thấy đường đi.",
                    icon="warning",
                )
                self.reset_app()
                return

            self.solution = path
            self.showing_solution = True
            self.algo_ran = True
            self.controls.lock_after_run()

            # Animate solution path
            for r, c in path:
                if not self.running:
                    break
                self.canvas.highlight_cell((r, c), "green", self.player, self.goal)
                self.root.after(50)
                self.root.update()

            # Animate player movement
            for r, c in path:
                if not self.running:
                    break
                self.player = (r, c)
                self.canvas.draw_player(self.player)
                self.root.after(100)
                self.root.update()

            if self.running:
                self.on_win()

        except Exception as e:
            traceback.print_exc()
            CTkMessagebox(
                title="Lỗi thuật toán",
                message=f"Có lỗi xảy ra khi chạy thuật toán:\n{e}",
                icon="cancel",
            )

        finally:
            self.running = False
            if not self.algo_ran:
                self.controls.set_controls_enabled(True)

    def reset_app(self):
        self.running = False
        self.player = START
        self.solution = None
        self.showing_solution = False
        self.algo_ran = False
        self.controls.set_controls_enabled(True)
        self.sidebar.update_metrics_table({})
        self.full_redraw()

    def random_maze(self, seed=None):
        global ROWS, COLS, START, GOAL
        ROWS, COLS = 21, 31
        self.maze, self.player, self.goal, used_seed = generate_random_maze(
            ROWS, COLS, seed
        )
        START, GOAL = self.player, self.goal
        self.sidebar.add_seed_to_history(used_seed)
        self.reset_app()
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE
        self.canvas.configure(width=canvas_w, height=canvas_h)

        rows, cols = len(self.maze), len(self.maze[0])

        # Sinh mê cung mới theo đúng kích thước hiện tại
        self.maze, self.player, self.goal, used_seed = generate_random_maze(rows, cols, seed)
        START, GOAL = self.player, self.goal

        self.sidebar.add_seed_to_history(used_seed)
        self.reset_app()

        # Cập nhật kích thước canvas
        canvas_w = cols * CELL_SIZE
        canvas_h = rows * CELL_SIZE
        self.canvas.config(width=canvas_w, height=canvas_h)
        self.full_redraw()

    def on_seed_double_click(self, seed):
        if self.running:
            CTkMessagebox(title="Đang chạy", message="Vui lòng đợi thuật toán kết thúc.")
            return

        try:
            self.random_maze(int(seed))
        except ValueError:
            CTkMessagebox(title="Lỗi seed", message=f"Seed '{seed}' không hợp lệ.", icon="warning")

    def toggle_grid_display(self):
        self.full_redraw()

    def set_custom_start(self):
        pos = ask_start_position(self.root, self.maze)
        if pos:
            self.player = pos
            self.full_redraw()

    def on_canvas_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        rows, cols = len(self.maze), len(self.maze[0])
        if 0 <= row < rows and 0 <= col < cols and self.maze[row][col] == 0:
            self.player = (row, col)
            self.full_redraw()
        else:
            CTkMessagebox(
                title="Không hợp lệ",
                message="Ô này không thể chọn làm vị trí bắt đầu.",
                icon="warning",
            )

    def change_maze_size(self, size_str):
        """Thay đổi kích thước mê cung và canh lại giao diện"""
        try:
            rows, cols = map(int, size_str.lower().split("x"))
        except ValueError:
            CTkMessagebox.showerror("Lỗi", f"Kích thước không hợp lệ: {size_str}")
            return

        global ROWS, COLS, START, GOAL
        ROWS, COLS = rows, cols

        # --- Sinh lại mê cung mới ---
        self.maze, start_pos, goal_pos, used_seed = generate_random_maze(ROWS, COLS)
        START, GOAL = start_pos, goal_pos

        # --- Đặt lại vị trí nhân vật về start mới ---
        self.player = start_pos
        self.goal = goal_pos

        # --- Đảm bảo player và goal không bị tường bao ---
        pr, pc = self.player
        gr, gc = self.goal
        self.maze[pr][pc] = 0
        self.maze[gr][gc] = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = gr + dr, gc + dc
            if 0 <= rr < ROWS and 0 <= cc < COLS:
                self.maze[rr][cc] = 0

        # --- Cập nhật kích thước canvas ---
        canvas_w = COLS * CELL_SIZE
        canvas_h = ROWS * CELL_SIZE
        self.canvas.config(width=canvas_w, height=canvas_h)

        # --- Reset giao diện nhưng giữ player ---
        self.solution = None
        self.showing_solution = False
        self.algo_ran = False
        self.running = False
        self.controls.set_controls_enabled(True)
        self.sidebar.update_metrics_table({})

        # --- Vẽ lại mê cung mới ---
        self.full_redraw()

        # --- Cập nhật bố cục (canvas + sidebar) ---
        self.root.update_idletasks()