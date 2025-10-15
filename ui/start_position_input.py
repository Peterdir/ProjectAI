import tkinter as tk
from tkinter import simpledialog, messagebox

def ask_start_position(root, maze):
    """
    Hộp thoại nhập toạ độ mới cho nhân vật.
    Trả về (row, col) hoặc None nếu người dùng bấm huỷ.
    """
    rows, cols = len(maze), len(maze[0])
    answer = simpledialog.askstring(
        "Đặt vị trí bắt đầu",
        f"Nhập toạ độ (hàng,cột), ví dụ: 3,5\nKích thước: {rows}x{cols}",
        parent=root
    )
    if not answer:
        return None

    try:
        r, c = map(int, answer.split(","))
        if not (0 <= r < rows and 0 <= c < cols):
            messagebox.showwarning("Sai toạ độ", "Toạ độ nằm ngoài mê cung.")
            return None
        if maze[r][c] == 1:
            messagebox.showwarning("Không hợp lệ", "Ô này là tường.")
            return None
        return (r, c)
    except:
        messagebox.showerror("Lỗi nhập", "Vui lòng nhập đúng định dạng: hàng,cột (ví dụ: 3,5)")
        return None
