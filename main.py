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
root.geometry("1000x600")

# ======================
# Tiêu đề
# ======================
Label(root, text="Maze Solver", font=("Arial", 20)).pack(pady=10)

# ======================
# Frame chứa combobox nhóm (xếp ngang trên cùng)
# ======================
top_frame = Frame(root)
top_frame.pack(fill="x", padx=10, pady=10)

# Hàm xử lý khi chọn thuật toán
def on_select(event, group_id):
    selected_algo = event.widget.get()
    messagebox.showinfo("Thông báo", f"Bạn chọn {selected_algo} trong Nhóm {group_id}")

# Tạo 6 nhóm, mỗi nhóm có combobox
for group in range(1, 7):
    frame = Frame(top_frame, padx=5, pady=5)
    frame.pack(side=LEFT, padx=5)

    Label(frame, text=f"Nhóm {group}", font=("Arial", 10, "bold")).pack()
    combo = ttk.Combobox(
        frame,
        values=[f"Thuật toán {i}" for i in range(1, 4)],
        state="readonly",
        width=15
    )
    combo.pack()
    combo.bind("<<ComboboxSelected>>", lambda e, g=group: on_select(e, g))

# ======================
# Frame hiển thị màn hình chạy (ở dưới)
# ======================
bottom_frame = Frame(root, relief="sunken", bd=2, height=400)
bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

Label(bottom_frame, text="Màn hình chạy sẽ hiển thị ở đây", font=("Arial", 14)).pack(pady=50)

# ======================
# Nút thoát
# ======================
Button(root, text="Thoát", command=root.quit).pack(pady=10)

# ======================
# Main loop
# ======================
root.mainloop()
