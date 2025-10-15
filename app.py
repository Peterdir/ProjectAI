from ui.maze_app import MazeApp
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = MazeApp(root)
    root.mainloop()
