# maze_solver/ui/sidebar.py
import tkinter as tk
from tkinter import ttk

class Sidebar(tk.Frame):
    def __init__(self, parent, on_seed_double_click_callback):
        super().__init__(parent)
        self.on_seed_double_click_callback = on_seed_double_click_callback
        self.setup_ui()

    def setup_ui(self):
        # Bảng hiển thị chỉ số thuật toán
        self.metrics_tree = ttk.Treeview(
            self, columns=("metric", "value"), show="headings", height=15
        )
        self.metrics_tree.heading("metric", text="Chỉ số")
        self.metrics_tree.heading("value", text="Giá trị")
        self.metrics_tree.column("metric", width=160, anchor="w")
        self.metrics_tree.column("value", width=180, anchor="center")

        metrics_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.metrics_tree.yview)
        self.metrics_tree.configure(yscrollcommand=metrics_scrollbar.set)
        self.metrics_tree.pack(side="top", fill="both", expand=True)
        metrics_scrollbar.pack(side="right", fill="y", before=self.metrics_tree)

        # Seed log
        tk.Label(self, text="Lịch sử Seed").pack(pady=(10, 0), anchor="w")
        seed_frame = tk.Frame(self)
        seed_frame.pack(fill="both", expand=False, padx=5, pady=5)
        self.seed_listbox = tk.Listbox(seed_frame, height=10)
        self.seed_listbox.pack(side="left", fill="both", expand=True)
        seed_scrollbar = tk.Scrollbar(seed_frame, orient="vertical", command=self.seed_listbox.yview)
        seed_scrollbar.pack(side="right", fill="y")
        self.seed_listbox.config(yscrollcommand=seed_scrollbar.set)
        self.seed_listbox.bind("<Double-1>", self.on_seed_double_click_callback)

        # Label seed hiện tại
        self.current_seed_label = tk.Label(self, text="Seed hiện tại: None")
        self.current_seed_label.pack(pady=(5, 10), anchor="w")

    def update_metrics_table(self, metrics, highlight_keys=[]):
        for item in self.metrics_tree.get_children():
            self.metrics_tree.delete(item)
        if not metrics: return
        for key, val in metrics.items():
            display_val = f"{val:.4f}" if isinstance(val, float) else val
            iid = self.metrics_tree.insert("", "end", values=(key, display_val))
            if key in highlight_keys:
                self.metrics_tree.item(iid, tags=("highlight"))
        self.metrics_tree.tag_configure("highlight", background="yellow")
        self.update()

    def add_seed_to_history(self, seed):
        seeds = list(self.seed_listbox.get(0, tk.END))
        s = str(seed)
        if s in seeds:
            idx = seeds.index(s)
            self.seed_listbox.delete(idx)
        self.seed_listbox.insert(tk.END, s)
        self.current_seed_label.config(text=f"Seed hiện tại: {seed}")