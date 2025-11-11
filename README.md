# 孤客截图工具 Pro 📸

一个简单易用、界面美观的桌面截图工具，支持区域截图、全屏截图、复制到剪贴板和保存图片等功能。

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## ✨ 功能特色

### 🎯 核心功能
- **🖼️ 区域截图** - 自由拖拽选择截图区域
- **🖥️ 全屏截图** - 一键截取整个屏幕
- **💾 保存截图** - 支持 PNG、JPEG 格式保存
- **📋 复制到剪贴板** - 快速复制截图到系统剪贴板
- **👀 实时预览** - 截图后立即预览效果

### 🎨 界面特色
- **现代化设计** - 简洁美观的圆角按钮设计
- **紧凑布局** - 小巧精致的界面，不占用桌面空间
- **中文界面** - 完全中文化的操作界面
- **状态提示** - 实时显示操作状态和提示信息

### ⚡ 便捷操作
- **设置菜单** - 快速访问常用功能
- **使用教程** - 内置详细的使用说明
- **反馈系统** - 一键跳转反馈页面

## 🚀 快速开始

### 环境要求
- Python 3.6 或更高版本
- Windows 操作系统

### 安装依赖

```bash
pip install pillow pywin32


运行程序
bash
python guke_screenshot_pro.py
📖 使用说明
基本操作
区域截图：点击"区域截图"按钮，拖拽鼠标选择区域

全屏截图：点击"全屏截图"按钮，自动截取整个屏幕

保存截图：截图后点击"保存截图"选择保存位置

复制截图：截图后点击"复制截图"粘贴到其他应用

快捷键
ESC - 取消截图操作

鼠标拖拽 - 选择截图区域

设置菜单
点击右上角的设置按钮(⚙)可以访问：

👤 关于作者 - 查看软件信息和开发者

⬇️ 下载最新版本 - 获取最新版本

📖 使用教程 - 查看详细使用说明

❓ 反馈问题 - 提交问题或建议

🗂️ 项目结构
text
guke-screenshot-pro/
├── guke_screenshot_pro.py    # 主程序文件
├── screenshot_settings.json  # 配置文件（自动生成）
├── screenshots/              # 截图保存目录（自动生成）
└── README.md                 # 说明文档
🔧 技术栈
GUI 框架：Tkinter (Python 内置)

图像处理：Pillow (PIL)

剪贴板操作：pywin32

界面设计：自定义圆角按钮和卡片布局

📝 更新日志
v2.0 (当前版本)
✅ 全新现代化界面设计

✅ 圆角按钮和卡片布局

✅ 设置菜单和快捷功能

✅ 实时截图预览

✅ 中文化操作界面

v1.0
✅ 基础截图功能

✅ 区域选择和全屏截图

✅ 图片保存和剪贴板复制

🤝 贡献指南
我们欢迎各种形式的贡献！

报告问题：通过 Issues 报告 bug 或提出建议

功能开发：Fork 项目并提交 Pull Request

文档改进：帮助改进文档或翻译

📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情

👨‍💻 开发者
孤客 - GitHub

如果这个项目对您有帮助，请给个 ⭐️ 支持一下！

🙏 致谢
感谢以下开源项目：

Pillow - 强大的图像处理库

pywin32 - Windows API 访问

注意：本工具目前主要支持 Windows 系统，其他系统可能需要调整剪贴板相关代码。

如有问题，请查看 使用教程 或提交 Issue。
text

## 额外建议的文件结构：

在您的项目文件夹中，建议包含以下文件：
guke-screenshot-pro/
├── guke_screenshot_pro.py # 主程序文件
├── requirements.txt # 依赖包列表
├── LICENSE # 许可证文件
├── README.md # 说明文档
├── screenshots/ # 截图示例目录
│ ├── main-ui.png
│ ├── screenshot-demo.png
│ └── settings-menu.png
└── .gitignore # Git 忽略文件
