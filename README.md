# KDEify - KDE Plasma 风格美化程序 for Windows

> 仿 Breeze 主题 + Dolphin 文件管理器 + Konsole 终端 + 系统主题调整

## 功能

| 模块 | 说明 |
|------|------|
| **文件管理器** | Dolphin 风格：侧边栏 Places、面包屑导航、三种视图、右键菜单、文件操作 |
| **Konsole 终端** | 多标签页终端：ANSI 颜色、快捷键、Shell 切换、字号调节 |
| **系统主题** | 深色/浅色模式、强调色、壁纸、任务栏设置、窗口边框 |
| **KDE 窗口装饰** | 无边框 + Breeze 风格标题栏（所有窗口统一风格） |

## 依赖

- Windows 10/11
- Python 3.10+
- PySide6
- PyInstaller（仅构建时需要）

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
# 启动器菜单
python main.py

# 直接打开某个模块
python main.py filemanager    # 文件管理器
python main.py konsole        # 终端
python main.py theme          # 系统主题
python main.py all            # 全部打开
```

## 打包为 .exe

```bash
pip install pyinstaller
python build.py
```

生成的 `dist/KDEify.exe` 可直接双击运行，无需 Python 环境。

## 目录结构

```
kdeify/
├── main.py                  # 入口
├── requirements.txt
├── build.py                 # PyInstaller 构建
├── README.md
└── kde/
    ├── app.py               # QApplication + 主题管理
    ├── theme.py             # Breeze QSS 样式
    ├── widgets/
    │   ├── frameless.py     # 无边框窗口 + 标题栏
    │   └── titlebar.py      # (已合并到 frameless.py)
    ├── filemanager/
    │   ├── window.py        # 文件管理器主窗口
    │   ├── sidebar.py       # Places 侧边栏
    │   ├── breadcrumb.py    # 面包屑导航
    │   └── filelist.py      # 文件列表
    ├── konsole/
    │   ├── window.py        # 终端主窗口
    │   └── terminal.py      # 终端控件
    └── system/
        └── themeadjust.py   # 系统主题调整
```

## 注意

- **系统主题调整**需要管理员权限
- 部分注册表修改后需注销/重启才能完全生效
- 终端模块在 Windows 上默认使用 `cmd.exe`，可切换 PowerShell/WSL
- 此程序不会修改 Explorer.exe，而是提供 KDE 风格的替代方案
