import customtkinter as ctk
from helpers.loader import discover_algorithms

class ControlsFrame(ctk.CTkFrame):
    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks
        self.selected_algo = ctk.StringVar()
        self.toggle_grid_var = ctk.BooleanVar(value=True)
        self.size_var = ctk.StringVar(value="21x31")
        self.algo_display_map = {}  # map hiển thị → module path
        self.setup_ui()

    def setup_ui(self):
        # Hàng 1
        self.show_btn = ctk.CTkButton(self, text="Show Solution", command=self.callbacks["show_solution"])
        self.show_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.reset_btn = ctk.CTkButton(self, text="Reset", command=self.callbacks["reset"])
        self.reset_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.grid_btn = ctk.CTkCheckBox(
            self,
            text="Grid lines",
            variable=self.toggle_grid_var,
            command=self.callbacks["toggle_grid"]
        )
        self.grid_btn.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        # Hàng 2
        self.setup_algo_menu()
        self.algo_menu.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        self.random_maze_btn = ctk.CTkButton(self, text="Random Mê Cung", command=self.callbacks["random_maze"])
        self.random_maze_btn.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Menu chọn kích thước mê cung
        sizes = ["10x10", "15x15", "21x31"]
        self.size_menu = ctk.CTkOptionMenu(
            self,
            variable=self.size_var,
            values=sizes,
            command=lambda value: self.callbacks["change_size"](value)
        )
        self.size_menu.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        self.grid_columnconfigure((0, 1, 2), weight=1)

    def setup_algo_menu(self):
        algos = discover_algorithms()
        grouped = {}

        # Gom nhóm theo thư mục con (info / noinfo / khác)
        for key in algos.keys():
            parts = key.replace("\\", "/").split("/")
            group = parts[0] if len(parts) > 1 else "Khác"
            algo = parts[-1]
            grouped.setdefault(group, []).append((algo, key))

        # Tạo danh sách hiển thị
        display_options = []
        for group, items in sorted(grouped.items()):
            for algo, full in sorted(items):
                display_name = f"{group} → {algo}"
                display_options.append(display_name)
                self.algo_display_map[display_name] = full

        if display_options:
            default_display = display_options[0]
            self.selected_algo.set(default_display)
        else:
            display_options = ["Không có thuật toán"]
            self.selected_algo.set(display_options[0])

        self.algo_menu = ctk.CTkOptionMenu(
            self,
            variable=self.selected_algo,
            values=display_options
        )

    def get_selected_algorithm_key(self):
        """Trả về key thật sự (ví dụ: 'info/astar') để load thuật toán."""
        return self.algo_display_map.get(self.selected_algo.get(), None)

    def set_controls_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.show_btn.configure(state=state)
        self.random_maze_btn.configure(state=state)
        self.algo_menu.configure(state=state)
        self.grid_btn.configure(state=state)
        self.reset_btn.configure(state="normal")  # Reset luôn bật

    def lock_after_run(self):
        self.show_btn.configure(state="disabled")
        self.random_maze_btn.configure(state="disabled")
        self.algo_menu.configure(state="disabled")
        self.grid_btn.configure(state="disabled")
        self.reset_btn.configure(state="normal")
