#!/usr/bin/env python3
"""
KDEify 构建脚本 - 使用 PyInstaller 打包为单个 .exe
"""
import PyInstaller.__main__
import os
import sys


def build():
    """打包 KDEify 为单文件 exe"""
    root = os.path.dirname(os.path.abspath(__file__))

    args = [
        os.path.join(root, "main.py"),
        "--name=KDEify",
        "--onefile",
        "--windowed",
        f"--distpath={os.path.join(root, 'dist')}",
        f"--workpath={os.path.join(root, 'build')}",
        "--clean",
        "--noconfirm",
        # 隐藏控制台
        "--disable-windowed-traceback",
    ]

    # Windows 下添加图标（如果有 ico 文件）
    ico = os.path.join(root, "resources", "kdeify.ico")
    if os.path.exists(ico):
        args.append(f"--icon={ico}")

    print("开始构建...")
    PyInstaller.__main__.run(args)
    print(f"构建完成！exe 位于: {os.path.join(root, 'dist', 'KDEify.exe')}")


if __name__ == "__main__":
    build()
