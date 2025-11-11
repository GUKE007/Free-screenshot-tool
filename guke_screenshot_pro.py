import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Frame, Label, Button
from PIL import ImageGrab, Image, ImageTk
import io
import os
import json
from datetime import datetime
import webbrowser


class GukeScreenshotPro:
    def __init__(self, root):
        self.root = root
        self.root.title("孤客截图工具 Pro")
        self.root.geometry("380x450")
        self.root.resizable(False, False)
        self.root.configure(bg='#f8f9fa')

        # 截图相关变量
        self.screenshot = None
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.screenshot_window = None
        self.canvas = None

        # 设置
        self.settings = self.load_settings()

        self.setup_ui()

    def load_settings(self):
        """加载设置"""
        default_settings = {
            "auto_save": False,
            "save_path": "screenshots",
            "format": "png",
            "quality": 95
        }
        return default_settings

    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_container = Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 标题栏
        title_frame = Frame(main_container, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 15))

        # 应用图标和标题
        icon_label = Label(title_frame, text="📸", font=('Arial', 20),
                           bg='#f8f9fa', fg='#6c5ce7')
        icon_label.pack(side=tk.LEFT)

        title_label = Label(title_frame, text="孤客截图工具 Pro",
                            font=('微软雅黑', 14, 'bold'),
                            fg='#2d3436', bg='#f8f9fa')
        title_label.pack(side=tk.LEFT, padx=(8, 0))

        # 设置按钮
        settings_btn = self.create_round_button(title_frame, "⚙",
                                                self.show_settings_menu,
                                                size=30, bg='#e84393')
        settings_btn.pack(side=tk.RIGHT)

        # 功能卡片
        self.create_function_card(main_container)

        # 预览卡片
        self.create_preview_card(main_container)

        # 状态栏
        self.create_status_bar(main_container)

    def create_round_button(self, parent, text, command, size=40, bg='#6c5ce7', fg='white'):
        """创建圆角按钮"""
        btn = Button(parent, text=text, command=command,
                     font=('Arial', 12), bg=bg, fg=fg, bd=0,
                     width=2, height=1, cursor='hand2')
        return btn

    def create_function_card(self, parent):
        """创建功能卡片"""
        card = Frame(parent, bg='white', relief='flat', bd=1,
                     highlightbackground='#dfe6e9', highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 12))

        # 卡片标题
        card_title = Label(card, text="✨ 快速操作", font=('微软雅黑', 11, 'bold'),
                           fg='#2d3436', bg='white')
        card_title.pack(anchor='w', padx=15, pady=(12, 8))

        # 按钮容器 - 2x3 网格
        btn_grid = Frame(card, bg='white')
        btn_grid.pack(fill=tk.X, padx=10, pady=(0, 12))

        # 第一行按钮
        row1 = Frame(btn_grid, bg='white')
        row1.pack(fill=tk.X, pady=4)

        self.screenshot_btn = self.create_function_button(row1, "🖼️\n区域截图",
                                                          self.start_screenshot, '#0984e3')
        self.screenshot_btn.pack(side=tk.LEFT, expand=True, padx=2)

        self.fullscreen_btn = self.create_function_button(row1, "🖥️\n全屏截图",
                                                          self.fullscreen_screenshot, '#00b894')
        self.fullscreen_btn.pack(side=tk.LEFT, expand=True, padx=2)

        self.save_btn = self.create_function_button(row1, "💾\n保存截图",
                                                    self.save_screenshot, '#fdcb6e')
        self.save_btn.pack(side=tk.LEFT, expand=True, padx=2)

        # 第二行按钮
        row2 = Frame(btn_grid, bg='white')
        row2.pack(fill=tk.X, pady=4)

        self.copy_btn = self.create_function_button(row2, "📋\n复制截图",
                                                    self.copy_to_clipboard, '#e17055')
        self.copy_btn.pack(side=tk.LEFT, expand=True, padx=2)

        self.history_btn = self.create_function_button(row2, "📚\n截图历史",
                                                       self.show_history, '#a29bfe')
        self.history_btn.pack(side=tk.LEFT, expand=True, padx=2)

        self.edit_btn = self.create_function_button(row2, "🎨\n图片编辑",
                                                    self.image_edit, '#fd79a8')
        self.edit_btn.pack(side=tk.LEFT, expand=True, padx=2)

    def create_function_button(self, parent, text, command, color):
        """创建功能按钮"""
        btn = Button(parent, text=text, command=command,
                     font=('微软雅黑', 9), bg=color, fg='white', bd=0,
                     width=8, height=3, cursor='hand2', justify=tk.CENTER,
                     relief='flat', overrelief='raised',
                     wraplength=60)
        return btn

    def create_preview_card(self, parent):
        """创建预览卡片"""
        card = Frame(parent, bg='white', relief='flat', bd=1,
                     highlightbackground='#dfe6e9', highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        # 卡片标题
        card_title = Label(card, text="👀 截图预览", font=('微软雅黑', 11, 'bold'),
                           fg='#2d3436', bg='white')
        card_title.pack(anchor='w', padx=15, pady=(12, 8))

        # 预览区域
        preview_frame = Frame(card, bg='#f1f2f6', relief='flat', bd=0, height=120)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        preview_frame.pack_propagate(False)

        self.preview_label = Label(preview_frame,
                                   text="暂无截图\n点击上方按钮开始截图",
                                   font=('微软雅黑', 9), fg='#636e72', bg='#f1f2f6',
                                   justify='center', wraplength=200)
        self.preview_label.pack(expand=True)

    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = Frame(parent, bg='#dfe6e9', relief='flat', bd=0, height=25)
        status_frame.pack(fill=tk.X, pady=(8, 0))
        status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(value="🟢 就绪 - 点击区域截图开始使用")
        status_label = Label(status_frame, textvariable=self.status_var,
                             font=('微软雅黑', 8), fg='#2d3436', bg='#dfe6e9')
        status_label.pack(side=tk.LEFT, padx=10, pady=4)

        # 版本信息
        version_label = Label(status_frame, text="v2.0 • 孤客制作",
                              font=('微软雅黑', 7), fg='#636e72', bg='#dfe6e9')
        version_label.pack(side=tk.RIGHT, padx=10, pady=4)

    def show_settings_menu(self):
        """显示设置菜单 - 修复对齐版本"""
        # 创建菜单窗口
        menu_window = tk.Toplevel(self.root)
        menu_window.title("设置菜单")
        menu_window.geometry("220x220")
        menu_window.configure(bg='white')
        menu_window.resizable(False, False)

        # 居中显示
        menu_window.transient(self.root)
        x = self.root.winfo_x() + (self.root.winfo_width() - 220) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 220) // 2
        menu_window.geometry(f"+{x}+{y}")

        # 菜单标题
        menu_title = Label(menu_window, text="⚙️ 设置菜单",
                           font=('微软雅黑', 12, 'bold'),
                           bg='white', fg='#2d3436')
        menu_title.pack(pady=(15, 10))

        # 菜单选项容器
        menu_frame = Frame(menu_window, bg='white')
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # 菜单选项 - 统一格式
        menu_items = [
            ("👤 关于作者", self.about_author),
            ("⬇️ 下载最新版本", self.download_latest),
            ("📖 使用教程", self.show_tutorial),
            ("❓ 反馈问题", self.feedback)
        ]

        for i, (text, command) in enumerate(menu_items):
            # 创建每个菜单项的容器
            item_frame = Frame(menu_frame, bg='white', height=35)
            item_frame.pack(fill=tk.X, pady=2)
            item_frame.pack_propagate(False)

            # 创建菜单按钮 - 统一使用相同的宽度和对齐方式
            btn = Button(item_frame, text=text, command=command,
                         font=('微软雅黑', 10), bg='white', fg='#2d3436', bd=0,
                         width=18, height=2, cursor='hand2', anchor='w',
                         relief='flat', justify='left')
            btn.pack(fill=tk.BOTH, padx=5)

            # 添加悬停效果
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#f8f9fa'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='white'))

            # 添加分隔线（除了最后一个）
            if i < len(menu_items) - 1:
                separator = Frame(item_frame, bg='#e0e0e0', height=1)
                separator.pack(fill=tk.X, side=tk.BOTTOM)

    def about_author(self):
        """关于作者"""
        about_text = """🎨 孤客截图工具 Pro

开发者: 孤客
版本: v2.0

一个简单易用的截图工具
支持区域截图、全屏截图
复制到剪贴板等功能

💝 感谢使用！"""
        messagebox.showinfo("关于作者", about_text)

    def download_latest(self):
        """下载最新版本"""
        download_url = "https://github.com/GUKE007/Free-screenshot-tool/releases/latest"
        webbrowser.open(download_url)
        messagebox.showinfo("下载", "正在打开下载页面...")

    def show_tutorial(self):
        """显示使用教程"""
        tutorial_text = """📚 使用教程

1. 🖼️ 区域截图
   - 点击"区域截图"按钮
   - 拖拽鼠标选择截图区域
   - 释放鼠标完成截图

2. 🖥️ 全屏截图
   - 点击"全屏截图"按钮
   - 自动截取整个屏幕

3. 💾 保存截图
   - 截图后点击"保存截图"
   - 选择保存位置和格式

4. 📋 复制截图
   - 截图后点击"复制截图"
   - 可直接粘贴到其他应用

💡 提示: 截图后可在预览区查看效果"""
        messagebox.showinfo("使用教程", tutorial_text)

    def feedback(self):
        """反馈问题"""
        feedback_url = "https://github.com/GUKE007/Free-screenshot-tool/issues"
        webbrowser.open(feedback_url)
        messagebox.showinfo("反馈", "正在打开反馈页面...")

    def start_screenshot(self):
        """开始截图"""
        self.root.withdraw()
        self.status_var.set("🎯 截图模式 - 拖拽鼠标选择区域")

        # 创建截图窗口
        self.create_screenshot_window()

    def create_screenshot_window(self):
        """创建截图窗口"""
        self.screenshot_window = tk.Toplevel(self.root)
        self.screenshot_window.attributes('-fullscreen', True)
        self.screenshot_window.attributes('-alpha', 0.3)
        self.screenshot_window.configure(background='black')
        self.screenshot_window.bind('<Escape>', lambda e: self.cancel_screenshot())

        # 创建画布
        self.canvas = tk.Canvas(self.screenshot_window, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 绑定事件
        self.canvas.bind('<Button-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

        # 显示提示
        self.canvas.create_text(self.screenshot_window.winfo_screenwidth() // 2,
                                30, text="拖拽鼠标选择截图区域 | ESC取消",
                                fill='white', font=('微软雅黑', 12, 'bold'))

    def on_mouse_press(self, event):
        """鼠标按下"""
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2, fill=''
        )

    def on_mouse_drag(self, event):
        """鼠标拖拽"""
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        """鼠标释放"""
        x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        if x2 - x1 > 10 and y2 - y1 > 10:
            self.take_screenshot(x1, y1, x2, y2)
        else:
            self.cancel_screenshot()

    def take_screenshot(self, x1, y1, x2, y2):
        """执行截图"""
        try:
            if self.screenshot_window:
                self.screenshot_window.destroy()

            self.screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            self.root.deiconify()

            # 更新预览
            self.update_preview()
            self.status_var.set("✅ 截图完成！")

        except Exception as e:
            messagebox.showerror("错误", f"截图失败: {e}")
            self.cancel_screenshot()

    def fullscreen_screenshot(self):
        """全屏截图"""
        try:
            self.screenshot = ImageGrab.grab()
            self.update_preview()
            self.status_var.set("✅ 全屏截图完成！")
        except Exception as e:
            messagebox.showerror("错误", f"全屏截图失败: {e}")

    def update_preview(self):
        """更新预览"""
        if self.screenshot:
            # 调整预览大小
            preview_size = (180, 100)
            preview_image = self.screenshot.copy()
            preview_image.thumbnail(preview_size, Image.Resampling.LANCZOS)

            # 转换为 PhotoImage
            photo = ImageTk.PhotoImage(preview_image)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo

    def save_screenshot(self):
        """保存截图"""
        if not self.screenshot:
            messagebox.showwarning("提示", "请先截图！")
            return

        # 确保保存目录存在
        save_dir = self.settings['save_path']
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"孤客截图_{timestamp}.{self.settings['format']}"
        filepath = os.path.join(save_dir, filename)

        try:
            self.screenshot.save(filepath, self.settings['format'].upper(),
                                 quality=self.settings['quality'])
            self.status_var.set(f"💾 已保存: {filename}")
            messagebox.showinfo("保存成功", f"截图已保存到:\n{filepath}")
        except Exception as e:
            messagebox.showerror("保存失败", f"错误: {e}")

    def copy_to_clipboard(self):
        """复制到剪贴板"""
        if not self.screenshot:
            messagebox.showwarning("提示", "请先截图！")
            return

        try:
            import win32clipboard
            from io import BytesIO

            output = BytesIO()
            self.screenshot.save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            self.status_var.set("📋 截图已复制到剪贴板")
            messagebox.showinfo("成功", "截图已复制到剪贴板！\n可以粘贴到其他应用了。")

        except ImportError:
            messagebox.showinfo("提示",
                                "复制功能需要安装 pywin32:\n请在命令行运行: pip install pywin32")
        except Exception as e:
            messagebox.showerror("复制失败", f"错误: {e}")

    def image_edit(self):
        """图片编辑（预留功能）"""
        messagebox.showinfo("图片编辑", "🎨 图片编辑功能正在开发中...")

    def show_history(self):
        """截图历史"""
        messagebox.showinfo("截图历史", "📚 截图历史功能正在开发中...")

    def cancel_screenshot(self):
        """取消截图"""
        if self.screenshot_window:
            self.screenshot_window.destroy()
        self.root.deiconify()
        self.status_var.set("❌ 截图已取消")


def main():
    root = tk.Tk()
    app = GukeScreenshotPro(root)

    # 窗口居中
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
