import tkinter as tk
from app import MazeApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.resizable(False, False)
    root.mainloop()
    