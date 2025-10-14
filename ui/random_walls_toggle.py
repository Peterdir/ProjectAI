# ui/random_walls_toggle.py
import tkinter as tk
from tkinter import ttk

class RandomWallsToggle(tk.Frame):
    def __init__(self, master, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback

        self.var = tk.BooleanVar(value=False)
        self.check = ttk.Checkbutton(
            self,
            text="Thêm tường ngẫu nhiên khi di chuyển",
            variable=self.var,
            command=self.on_toggle,
            style="Switch.TCheckbutton"
        )
        self.check.pack(anchor="w", padx=5, pady=5)

    def on_toggle(self):
        """Kích hoạt callback khi người dùng bật/tắt."""
        if self.callback:
            self.callback(self.var.get())

    def is_enabled(self):
        """Trả về True nếu toggle đang bật."""
        return self.var.get()

    def set_state(self, state: bool):
        """Thay đổi trạng thái toggle bằng code."""
        self.var.set(state)
        if self.callback:
            self.callback(state)
