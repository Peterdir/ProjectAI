import tkinter as tk
from helpers.loader import discover_algorithms

class ControlsFrame(tk.Frame):
    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks
        self.selected_algo = tk.StringVar()
        self.toggle_grid_var = tk.BooleanVar(value=True)
        self.setup_ui()

    def setup_ui(self):
        # Hàng 1
        self.show_btn = tk.Button(self, text="Show Solution", command=self.callbacks["show_solution"])
        self.show_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.reset_btn = tk.Button(self, text="Reset", command=self.callbacks["reset"])
        self.reset_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.grid_btn = tk.Checkbutton(self, text="Grid lines", var=self.toggle_grid_var, command=self.callbacks["toggle_grid"])
        self.grid_btn.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        # Hàng 2
        self.setup_algo_menu()
        self.algo_menu.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.random_maze_btn = tk.Button(self, text="Random Mê Cung", command=self.callbacks["random_maze"])
        self.random_maze_btn.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        self.grid_columnconfigure((0,1,2), weight=1)

    def setup_algo_menu(self):
        algos = discover_algorithms()
        self.algo_menu = tk.Menubutton(self, text="Chọn thuật toán", relief="raised")
        menu = tk.Menu(self.algo_menu, tearoff=0)
        self.algo_menu["menu"] = menu

        grouped = {}
        for key in algos.keys():
            group, *algo_parts = key.replace("\\", "/").split("/")
            algo = "/".join(algo_parts) if algo_parts else group
            if not algo_parts: group = "Khác"
            grouped.setdefault(group, []).append((algo, key))

        for group, items in sorted(grouped.items()):
            submenu = tk.Menu(menu, tearoff=0)
            for name, full_path in sorted(items):
                submenu.add_radiobutton(label=name, variable=self.selected_algo, value=full_path)
            menu.add_cascade(label=group, menu=submenu)
        
        if algos:
            self.selected_algo.set(next(iter(algos.keys())))

    def set_controls_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.show_btn.config(state=state)
        self.random_maze_btn.config(state=state)
        self.algo_menu.config(state=state)
        self.grid_btn.config(state=state)
        self.reset_btn.config(state="normal") # Reset luôn bật

    def lock_after_run(self):
        self.show_btn.config(state="disabled")
        self.random_maze_btn.config(state="disabled")
        self.algo_menu.config(state="disabled")
        self.grid_btn.config(state="disabled")
        self.reset_btn.config(state="normal")