# 版权信息
# 即现（信阳）网络科技有限公司 版权所有
# https://www.jixiannet.com
# 2024年06月06日
import tkinter as tk
from tkinter import filedialog, messagebox
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import os
from PIL import ImageTk
from urllib.parse import unquote

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 8765
server_instance = None  # 存储HTTP服务器实例的引用
stop_event = threading.Event()  # 控制HTTP服务器退出的事件标志

def select_folder():
    """选择文件夹的回调函数。"""
    folder_selected = filedialog.askdirectory()
    entry_folder_path.delete(0, tk.END)
    entry_folder_path.insert(0, folder_selected)


class GracefulHTTPRequestHandler(BaseHTTPRequestHandler):
    def translate_path(self, path):
        global folder_path
        return os.path.join(folder_path, path.lstrip('/'))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True  # 设置线程为守护进程，随主程序结束而结束


def serve_http():
    """启动HTTP文件服务器的回调函数，运行在新线程内。"""
    global server_thread
    folder_path = entry_folder_path.get()
    ip = entry_ip.get()
    port = int(entry_port.get())

    if not os.path.isdir(folder_path):
        messagebox.showerror("错误", "请选择一个有效的文件夹路径")
        return

    class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
        def translate_path(self, path):
            # 使用unquote对路径进行解码，确保中文等字符能够正确处理
            path = unquote(path, errors='ignore')
            folder_path = entry_folder_path.get()  # 获取文件夹路径
            return os.path.join(folder_path, path.lstrip('/'))

    handler = CustomHTTPRequestHandler

    try:
        server_address = (ip, port)
        httpd = HTTPServer(server_address, handler)
        sa = httpd.socket.getsockname()
        print(f"Serving HTTP on {sa[0]} port {sa[1]} ...")
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True  # 设置为守护线程，主程序结束时自动结束
        server_thread.start()
    except Exception as e:
        messagebox.showerror("错误", str(e))


def start_http_server():
    """启动HTTP文件服务器的回调函数，运行在新线程内。"""
    global folder_path
    folder_path = entry_folder_path.get()
    if not os.path.isdir(folder_path):
        messagebox.showerror("错误", "请选择一个有效的文件夹路径")
        return

    thread = threading.Thread(target=serve_http, daemon=True)
    thread.start()


def stop_http_server():
    """停止HTTP服务器的函数。"""
    global stop_event, server_instance
    stop_event.set()  # 设置事件，通知服务器线程停止
    if server_instance:
        server_instance.shutdown()  # 使用shutdown方法优雅关闭服务器
        server_instance.server_close()  # 关闭服务器的socket
        server_instance = None


def on_closing():
    """窗口关闭时调用的函数，确保HTTP服务器线程被正确停止。"""
    stop_http_server()
    root.quit()  # 使用quit而非destroy，以确保Tkinter主循环正常结束


# 创建GUI
root = tk.Tk()
root.title("即传 - 文件共享工具 V1.0")
# 在这里先不设置窗口大小，等到计算居中后再设置

# 设置图标（使用PNG文件）
image = ImageTk.PhotoImage(file="logo.png")  # 确保logo.png在当前目录
root.iconphoto(True, image)

# 绑定窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 自定义样式
style = {'font': ('Arial', 12), 'bg': '#F0F0F0', 'fg': '#333333'}

tk.Label(root, text="监听IP地址", **style).pack(pady=5)
entry_ip = tk.Entry(root, **style)
entry_ip.pack(fill=tk.X, padx=20)
entry_ip.insert(tk.END, DEFAULT_IP)

tk.Label(root, text="端口", **style).pack(pady=5)
entry_port = tk.Entry(root, **style)
entry_port.pack(fill=tk.X, padx=20)
entry_port.insert(tk.END, str(DEFAULT_PORT))

tk.Label(root, text="选择文件夹", **style).pack(pady=5)
entry_folder_path = tk.Entry(root, **style)
entry_folder_path.pack(fill=tk.X, padx=20)

browse_button = tk.Button(root, text="浏览", command=select_folder, bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10,
                          pady=5, font=('Arial', 10))
browse_button.pack(pady=5)

start_share_button = tk.Button(root, text="开始共享", command=start_http_server, bg="#007bff", fg="white",
                               relief=tk.FLAT, padx=10, pady=5, font=('Arial', 10))
start_share_button.pack(pady=10)

# 更新窗口配置，确保所有配置都已经应用
root.update_idletasks()

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 获取窗口宽度和高度
# = root.winfo_width()
#window_height = root.winfo_height()
# 获取窗口宽度和高度
window_width = 350
window_height = 260

# 计算居中位置
x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))

# 设置窗口大小和位置
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

root.mainloop()