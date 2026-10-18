#!/usr/bin/env python3
"""
KDEify - KDE Plasma 风格美化程序 for Windows
================================================
启动器：选择要打开的功能模块。

用法：
    python main.py                  # 启动器菜单
    python main.py filemanager      # 直接打开文件管理器
    python main.py konsole          # 直接打开终端
    python main.py theme            # 打开系统主题调整
    python main.py all              # 全部打开
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kde.app import KDEApplication
from kde.filemanager.window import FileManagerWindow
from kde.konsole.window import KonsoleWindow
from kde.system.themeadjust import ThemeAdjustWindow


def main():
    app = KDEApplication(sys.argv)
    app.apply_theme()

    args = sys.argv[1:]
    mode = args[0] if args else "launcher"

    windows = []

    if mode in ("filemanager", "all"):
        fm = FileManagerWindow()
        fm.show()
        windows.append(fm)

    if mode in ("konsole", "all"):
        kt = KonsoleWindow()
        kt.show()
        windows.append(kt)

    if mode in ("theme", "all"):
        ta = ThemeAdjustWindow()
        ta.show()
        windows.append(ta)

    if mode == "launcher":
        from PySide6.QtWidgets import QInputDialog
        items = [
            "文件管理器 (Dolphin 风格)",
            "Konsole 终端",
            "系统主题调整",
            "全部打开",
        ]
        item, ok = QInputDialog.getItem(
            None, "KDEify", "选择要打开的功能：", items, 0, False
        )
        if not ok:
            return
        if item == items[0]:
            FileManagerWindow().show()
        elif item == items[1]:
            KonsoleWindow().show()
        elif item == items[2]:
            ThemeAdjustWindow().show()
        elif item == items[3]:
            FileManagerWindow().show()
            KonsoleWindow().show()
            ThemeAdjustWindow().show()

    if not windows and mode != "launcher":
        print(f"未知模式: {mode}")
        print("可用: filemanager, konsole, theme, all")
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
