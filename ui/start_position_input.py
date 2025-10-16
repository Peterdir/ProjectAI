import customtkinter as ctk

from CTkMessagebox import CTkMessagebox

def ask_start_position(root, maze):
    """
    Hộp thoại nhập toạ độ mới cho nhân vật.
    Trả về (row, col) hoặc None nếu người dùng bấm huỷ.
    """
    rows, cols = len(maze), len(maze[0])

    # Tạo cửa sổ con CTk thay vì simpledialog
    dialog = ctk.CTkToplevel(root)
    dialog.title("Đặt vị trí bắt đầu")
    dialog.geometry("300x180")
    dialog.resizable(False, False)
    dialog.grab_set()  # chặn thao tác với cửa sổ cha

    label = ctk.CTkLabel(
        dialog,
        text=f"Nhập toạ độ (hàng,cột)\nVí dụ: 3,5\nKích thước: {rows}x{cols}",
        justify="center"
    )
    label.pack(pady=(20, 10))

    entry = ctk.CTkEntry(dialog, placeholder_text="hàng,cột")
    entry.pack(padx=20, pady=5)

    result = {"value": None}

    def on_confirm():
        answer = entry.get()
        if not answer:
            dialog.destroy()
            return

        try:
            r, c = map(int, answer.split(","))
            if not (0 <= r < rows and 0 <= c < cols):
                CTkMessagebox.showwarning("Sai toạ độ", "Toạ độ nằm ngoài mê cung.")
                return
            if maze[r][c] == 1:
                CTkMessagebox.showwarning("Không hợp lệ", "Ô này là tường.")
                return
            result["value"] = (r, c)
            dialog.destroy()
        except:
            CTkMessagebox.showerror("Lỗi nhập", "Vui lòng nhập đúng định dạng: hàng,cột (ví dụ: 3,5)")

    def on_cancel():
        dialog.destroy()

    # Nút bấm
    btn_frame = ctk.CTkFrame(dialog)
    btn_frame.pack(pady=15)

    ctk.CTkButton(btn_frame, text="Xác nhận", command=on_confirm, width=100).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Huỷ", command=on_cancel, width=80).pack(side="left", padx=10)

    # Chờ đến khi đóng dialog
    root.wait_window(dialog)

    return result["value"]
