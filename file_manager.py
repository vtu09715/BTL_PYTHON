import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Hàm để liệt kê file
def show_files():
    folder = filedialog.askdirectory()
    if not folder:
        return

    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        messagebox.showerror("Lỗi", f"Không tìm thấy đường dẫn: {folder}")
        return

    tree.delete(*tree.get_children())

    for file in files:
        filepath = os.path.join(folder, file)
        if os.path.isfile(filepath):
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.txt', '.py', '.jpg']:
                tree.insert("", "end", values=(file, ext, filepath))

# Hàm mở file
def open_selected_file():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chú ý", "Chưa chọn file để mở.")
        return

    filepath = tree.item(selected, "values")[2]
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".py":
            subprocess.Popen([sys.executable, "-m", "idlelib", filepath])
        else:
            os.startfile(filepath)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không mở được file: {e}")

# Double-click để mở file
def on_double_click(event):
    open_selected_file()

# Giao diện chính
root = tk.Tk()
root.title("Trình Quản Lý Thư Mục GUI")

# Nút chọn thư mục và mở
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="x")

btn_select = tk.Button(frame, text="Chọn thư mục", command=show_files)
btn_select.pack(side="left")

btn_open = tk.Button(frame, text="Mở", command=open_selected_file)
btn_open.pack(side="right")

# Bảng danh sách file
columns = ("Tên file", "Loại", "Đường dẫn")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(padx=10, pady=10, fill="both", expand=True)
tree.bind("<Double-1>", on_double_click)

root.mainloop()
