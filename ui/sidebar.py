import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, on_seed_double_click_callback):
        super().__init__(parent)
        self.on_seed_double_click_callback = on_seed_double_click_callback
        self.setup_ui()

    def setup_ui(self):
        # Bảng hiển thị chỉ số thuật toán
        self.metrics_frame = ctk.CTkFrame(self)
        self.metrics_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.metrics_label = ctk.CTkLabel(self.metrics_frame, text="Chỉ số thuật toán", font=ctk.CTkFont(size=14, weight="bold"))
        self.metrics_label.pack(pady=(0, 5))

        self.metrics_box = ctk.CTkTextbox(self.metrics_frame, height=250, wrap="none")
        self.metrics_box.pack(fill="both", expand=True)

        # Seed log
        ctk.CTkLabel(self, text="Lịch sử Seed", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(10, 0), anchor="w")

        seed_frame = ctk.CTkFrame(self)
        seed_frame.pack(fill="both", expand=False, padx=5, pady=5)

        self.seed_listbox = ctk.CTkTextbox(seed_frame, height=100, wrap="none")
        self.seed_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(seed_frame, orientation="vertical", command=self._on_scroll)
        scrollbar.pack(side="right", fill="y")
        self.seed_listbox._textbox.configure(yscrollcommand=scrollbar.set)  # hack nhẹ để sync scrollbar CTkTextbox
        self.seed_listbox.bind("<Double-1>", self.on_seed_click)

        # Label seed hiện tại
        self.current_seed_label = ctk.CTkLabel(self, text="Seed hiện tại: None")
        self.current_seed_label.pack(pady=(5, 10), anchor="w")

    def _on_scroll(self, *args):
        self.seed_listbox._textbox.yview(*args)

    def update_metrics_table(self, metrics, highlight_keys=[]):
        self.metrics_box.configure(state="normal")
        self.metrics_box.delete("1.0", "end")
        if not metrics:
            self.metrics_box.configure(state="disabled")
            return
        for key, val in metrics.items():
            display_val = f"{val:.4f}" if isinstance(val, float) else val
            line = f"{key}: {display_val}\n"
            self.metrics_box.insert("end", line)
            if key in highlight_keys:
                self.metrics_box.tag_add(key, f"{float(self.metrics_box.index('end')) - 2} linestart", "end")
                self.metrics_box.tag_config(key)
        self.metrics_box.configure(state="disabled")

    def add_seed_to_history(self, seed):
        text = self.seed_listbox.get("1.0", "end").strip().split("\n")
        s = str(seed)
        if s in text:
            text.remove(s)
        text.append(s)
        self.seed_listbox.configure(state="normal")
        self.seed_listbox.delete("1.0", "end")
        self.seed_listbox.insert("end", "\n".join(text))
        self.seed_listbox.configure(state="disabled")
        self.current_seed_label.configure(text=f"Seed hiện tại: {seed}")

    def on_seed_click(self, event):
        widget = event.widget
        index = widget.index(f"@{event.x},{event.y}")
        line_number = int(index.split(".")[0])
        line = widget.get(f"{line_number}.0", f"{line_number}.end").strip()
        if line:
            self.on_seed_double_click_callback(line)
