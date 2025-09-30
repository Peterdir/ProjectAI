# ======================
# main.py
# ======================

# Thư viện Tkinter (giao diện)
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# Thư viện xử lý ảnh cho Tkinter
from PIL import Image, ImageTk

# ======================
# Khởi tạo cửa sổ chính
# ======================
root = Tk()
root.title("Demo Tkinter GUI")
root.geometry("800x600")

# ======================
# Thêm các widget cơ bản (demo)
# ======================
Label(root, text="Xin chào 👋", font=("Arial", 20)).pack(pady=20)

Button(root, text="Thoát", command=root.quit).pack(pady=10)

# ======================
# Main loop
# ======================
root.mainloop()
