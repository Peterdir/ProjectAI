# Mê Cung Tkinter có lời giải

## 1. Cấu trúc dự án

```text
.
├── assets
│   ├── goal.png
│   ├── player.png
│   ├── wall.png
├── helpers
│   ├── algorithms
│   │   ├── astar.py
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── dls.py
│   │   ├── ids.py
│   │   ├── ucs.py
│   ├── loader.py
├── .gitignore
├── app.py
├── config.py
├── __main__.py
├── README.md
```

## 2. Yêu cầu hệ thống

* **Python** 3.8+ (khuyến nghị 3.10 trở lên)
* **Pip** để cài thư viện
* Các thư viện:

  * **Tkinter** (GUI)
  * **Pillow** (xử lý ảnh PNG)

## 3. Cài đặt và chạy

```bash
git clone https://github.com/Peterdir/ProjectAI/tree/maze-tamida
pip install pillow tkinter
```

Chạy ứng dụng:

* **Windows (PowerShell / CMD):**

```powershell
python .\__main__.py
```

* **macOS / Linux:**

```bash
python3 __main__.py
```

* **VS Code:** mở thư mục dự án → mở `__main__.py` → Run (hoặc Code Runner `Ctrl+Alt+N`).

> **Lưu ý:** Chạy từ **thư mục gốc** của dự án để đảm bảo đường dẫn `assets/*.png` load đúng.

## 4. Tính năng chính

* Giao diện Tkinter trực quan với ảnh nhân vật (`player.png`), đích (`goal.png`) và tường (`wall.png`).
* Điều khiển người chơi bằng **phím mũi tên** hoặc **WASD**.
* Nút **Show Solution**: hiển thị đường đi ngắn nhất (theo thuật toán chọn).
* Nút **Reset**: đưa người chơi về vị trí ban đầu.
* Tùy chọn **Grid lines** để bật/tắt lưới.
* Hỗ trợ nhiều **thuật toán tìm đường**: BFS, DFS, DLS, IDS, UCS, A\*…
* Menu chọn thuật toán tự động load từ thư mục `helpers/algorithms`.

## 5. Các tệp quan trọng

* `config.py`: cấu hình mê cung (`ROWS`, `COLS`, `CELL_SIZE`, `START`, `GOAL`, `MAZE`, màu sắc…).
* `helpers/algorithms/*.py`: mỗi file chứa một thuật toán tìm đường (`find_path`).
* `helpers/loader.py`: tự động load thuật toán theo tên.
* `app.py`: giao diện Tkinter, vẽ mê cung, người chơi, và xử lý sự kiện.
* `__main__.py`: file entry point, chạy app.

---

## Liên hệ

Nếu có thắc mắc về code, bạn có thể liên hệ mình qua:

<p align="center">
  <a href="mailto:dmt826321@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?logo=gmail&logoColor=white&style=for-the-badge"/></a>
  <a href="https://facebook.com/tamidanopro"><img src="https://img.shields.io/badge/Facebook-1877F2?logo=facebook&logoColor=white&style=for-the-badge"/></a>
  <a href="https://github.com/dangminhtai"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white&style=for-the-badge"/></a>
</p>

> Thả 1 star ⭐ nếu cảm thấy dự án này hữu ích nhé!
