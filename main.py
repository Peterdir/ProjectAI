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
top_frame.pack(fill="x", padx=10, pady=10) # Khung trên kéo dài ngang (fill="x")


# ======================
# Frame chứa các nút điều khiển (xếp ở góc trên bên phải)
# ======================
control_frame = Frame(top_frame)
control_frame.pack(fill="x", pady=(0, 10))

Button(control_frame, text="Start", width=8, command=lambda: print("Start clicked")).pack(side=LEFT, padx=20)
Button(control_frame, text="Reset", width=8, command=lambda: print("Reset clicked")).pack(side=LEFT, padx=20)
Button(control_frame, text="Stop", width=8, command=lambda: print("Stop clicked")).pack(side=LEFT, padx=20)
# Hàm xử lý khi chọn thuật toán
def on_select(event, group_id):
    selected_algo = event.widget.get()
    messagebox.showinfo("Thông báo", f"Bạn chọn {selected_algo} trong Nhóm {group_id}")

# ======================
# Danh sách thuật toán theo nhóm
# ======================
algorithms = {
    1: ["BFS", "DFS", "IDS"],
    2: ["Greedy Best First", "A*", "UCS"],
    3: ["Hill Climbing", "Simulated Annealing", "Genetic Algorithm"],
    4: ["Backtracking", "Branch and Bound", "Constraint Propagation"],
    5: ["Dynamic Programming", "Floyd-Warshall", "Dijkstra"],
    6: ["Bellman-Ford", "Johnson’s Algorithm", "Warshall’s Algorithm"]
}

# Tạo 6 nhóm, mỗi nhóm có combobox
for group in range(1, 7):
    frame = Frame(top_frame, padx=5, pady=5)
    frame.pack(side=LEFT, padx=5, expand=True)

    Label(frame, text=f"Nhóm {group}", font=("Arial", 10, "bold")).pack()
    combo = ttk.Combobox(
        frame,
        values=algorithms[group],
        state="readonly", # Chỉ cho chọn, không cho gõ
        width=15
    )
    combo.pack(fill="x")
    combo.bind("<<ComboboxSelected>>", lambda e, g=group: on_select(e, g)) # Gắn sự kiện khi chọn thuật toán

# ======================
# Frame hiển thị màn hình chạy (ở dưới)
# ======================
bottom_frame = Frame(root, relief="sunken", bd=2, height=400) # Tạo viền cho khung
bottom_frame.pack(fill="both", expand=True, padx=10, pady=10) # Chiếm toàn bộ phần còn lại của cửa sổ

Label(bottom_frame, text="Màn hình chạy sẽ hiển thị ở đây", font=("Arial", 14)).pack(pady=50)

# ======================
# Nút thoát
# ======================
Button(root, text="Thoát", command=root.quit).pack(pady=10)

# ======================
# Main loop
# ======================
root.mainloop()
