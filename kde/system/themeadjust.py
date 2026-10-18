"""
系统主题调整 - 通过修改 Windows 注册表实现 KDE 风格化。

注意：
    - 需要管理员权限才能修改部分注册表项
    - 修改后可能需要重新登录或重启才生效
    - 提供"还原"功能恢复默认值
"""
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QComboBox, QLineEdit,
    QCheckBox, QColorDialog, QFileDialog, QMessageBox,
    QFormLayout, QScrollArea, QFrame, QApplication,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QStyle

from ..widgets.frameless import FramelessWindow


class ThemeAdjustWindow(FramelessWindow):
    """系统主题调整窗口"""

    def __init__(self):
        super().__init__("系统主题调整 — KDEify", 520, 640)
        self._setup_titlebar()
        self._setup_ui()

    def _setup_titlebar(self):
        self.set_window_icon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton))

    def _setup_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ── 主题模式 ──
        grp_mode = QGroupBox("外观模式", self)
        mode_layout = QFormLayout(grp_mode)

        self.dark_check = QCheckBox("深色模式 (Breeze Dark)", self)
        self.dark_check.stateChanged.connect(self._on_dark_changed)
        mode_layout.addRow(self.dark_check)

        layout.addWidget(grp_mode)

        # ── 强调色 ──
        grp_accent = QGroupBox("强调色", self)
        accent_layout = QFormLayout(grp_accent)

        self.accent_btn = QPushButton("选择颜色...", self)
        self.accent_btn.clicked.connect(self._pick_accent)
        self.accent_color = QColor("#3daee9")
        self._update_accent_preview()
        accent_layout.addRow("窗口高亮色:", self.accent_btn)

        self.accent_label = QLabel(self)
        self.accent_label.setFixedHeight(24)
        accent_layout.addRow("当前颜色:", self.accent_label)

        layout.addWidget(grp_accent)

        # ── 任务栏 ──
        grp_taskbar = QGroupBox("任务栏", self)
        tb_layout = QFormLayout(grp_taskbar)

        self.taskbar_pos = QComboBox(self)
        self.taskbar_pos.addItems(["底部 (默认)", "顶部", "左侧", "右侧"])
        tb_layout.addRow("位置:", self.taskbar_pos)

        self.taskbar_transparent = QCheckBox("透明任务栏", self)
        tb_layout.addRow(self.taskbar_transparent)

        self.taskbar_small = QCheckBox("小图标", self)
        tb_layout.addRow(self.taskbar_small)

        layout.addWidget(grp_taskbar)

        # ── 壁纸 ──
        grp_wallpaper = QGroupBox("桌面壁纸", self)
        wp_layout = QFormLayout(grp_wallpaper)

        self.wallpaper_path = QLineEdit(self)
        wp_layout.addRow("壁纸路径:", self.wallpaper_path)

        wp_btn_layout = QHBoxLayout()
        btn_browse = QPushButton("浏览...", self)
        btn_browse.clicked.connect(self._browse_wallpaper)
        wp_btn_layout.addWidget(btn_browse)
        btn_apply_wp = QPushButton("应用", self)
        btn_apply_wp.clicked.connect(self._apply_wallpaper)
        wp_btn_layout.addWidget(btn_apply_wp)
        wp_layout.addRow("", wp_btn_layout)

        self.wp_style = QComboBox(self)
        self.wp_style.addItems(["填充", "适应", "拉伸", "平铺", "居中", "跨区"])
        wp_layout.addRow("显示方式:", self.wp_style)

        layout.addWidget(grp_wallpaper)

        # ── 窗口边框 ──
        grp_border = QGroupBox("窗口边框", self)
        border_layout = QFormLayout(grp_border)

        self.border_color_btn = QPushButton("边框颜色...", self)
        self.border_color_btn.clicked.connect(self._pick_border_color)
        self.border_color = QColor("#3daee9")
        self._update_border_preview()
        border_layout.addRow("颜色:", self.border_color_btn)

        self.border_label = QLabel(self)
        self.border_label.setFixedHeight(24)
        border_layout.addRow("当前:", self.border_label)

        self.border_width = QComboBox(self)
        self.border_width.addItems(["1px", "2px", "3px", "0px (无边框)"])
        border_layout.addRow("宽度:", self.border_width)

        layout.addWidget(grp_border)

        # ── 字体 ──
        grp_font = QGroupBox("系统字体", self)
        font_layout = QFormLayout(grp_font)

        self.font_combo = QComboBox(self)
        self.font_combo.addItems([
            "Segoe UI", "Microsoft YaHei UI", "Noto Sans CJK SC",
            "Noto Sans", "JetBrains Mono", "Cascadia Mono",
        ])
        font_layout.addRow("字体:", self.font_combo)

        self.font_size = QComboBox(self)
        self.font_size.addItems(["9", "10", "11", "12"])
        font_layout.addRow("大小:", self.font_size)

        layout.addWidget(grp_font)

        layout.addStretch()

        # ── 操作按钮 ──
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_apply = QPushButton("全部应用", self)
        btn_apply.clicked.connect(self._apply_all)
        btn_layout.addWidget(btn_apply)

        btn_reset = QPushButton("恢复默认", self)
        btn_reset.clicked.connect(self._reset_defaults)
        btn_layout.addWidget(btn_reset)

        btn_restart = QPushButton("重启资源管理器", self)
        btn_restart.clicked.connect(self._restart_explorer)
        btn_layout.addWidget(btn_restart)

        layout.addLayout(btn_layout)

        scroll.setWidget(container)
        self.set_content(scroll)

    def _update_accent_preview(self):
        self.accent_label.setStyleSheet(
            f"background-color: {self.accent_color.name()}; border-radius: 3px;"
        )

    def _update_border_preview(self):
        self.border_label.setStyleSheet(
            f"background-color: {self.border_color.name()}; border-radius: 3px;"
        )

    def _pick_accent(self):
        color = QColorDialog.getColor(self.accent_color, self, "选择强调色")
        if color.isValid():
            self.accent_color = color
            self._update_accent_preview()

    def _pick_border_color(self):
        color = QColorDialog.getColor(self.border_color, self, "选择边框颜色")
        if color.isValid():
            self.border_color = color
            self._update_border_preview()

    def _on_dark_changed(self, state):
        pass  # 由 _apply_all 统一应用

    def _browse_wallpaper(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择壁纸", "",
            "图片 (*.jpg *.jpeg *.png *.bmp);;所有文件 (*)"
        )
        if path:
            self.wallpaper_path.setText(path)

    def _apply_wallpaper(self):
        path = self.wallpaper_path.text().strip()
        if not path:
            QMessageBox.warning(self, "提示", "请先选择壁纸文件")
            return
        try:
            import ctypes
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, path, 3
            )
            QMessageBox.information(self, "成功", "壁纸已应用")
        except Exception as e:
            QMessageBox.warning(self, "失败", str(e))

    def _apply_all(self):
        """应用所有设置"""
        if sys.platform != "win32":
            QMessageBox.information(self, "提示", "此功能仅支持 Windows")
            return

        try:
            import winreg

            # 打开注册表键
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                0, winreg.KEY_SET_VALUE
            )

            # 深色模式
            if self.dark_check.isChecked():
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            else:
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 1)

            # 强调色
            r, g, b = self.accent_color.red(), self.accent_color.green(), self.accent_color.blue()
            color_value = r | (g << 8) | (b << 16)
            winreg.SetValueEx(key, "ColorPrevalence", 0, winreg.REG_DWORD, 1)

            key2 = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Control Panel\Colors",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key2, "Highlight", 0, winreg.REG_SZ,
                              f"{r} {g} {b}")

            winreg.CloseKey(key)
            winreg.CloseKey(key2)

            QMessageBox.information(
                self, "成功",
                "设置已应用。部分更改可能需要注销或重启才能完全生效。"
            )
        except PermissionError:
            QMessageBox.warning(
                self, "权限不足",
                "需要管理员权限。请以管理员身份重新运行此程序。"
            )
        except Exception as e:
            QMessageBox.warning(self, "错误", str(e))

    def _reset_defaults(self):
        """恢复默认设置"""
        if sys.platform != "win32":
            return
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)

            self.dark_check.setChecked(False)
            self.accent_color = QColor("#3daee9")
            self._update_accent_preview()
            QMessageBox.information(self, "成功", "已恢复默认设置")
        except Exception as e:
            QMessageBox.warning(self, "错误", str(e))

    def _restart_explorer(self):
        """重启资源管理器"""
        if sys.platform != "win32":
            return
        try:
            import subprocess
            subprocess.run(["taskkill", "/f", "/im", "explorer.exe"],
                           capture_output=True)
            subprocess.Popen("explorer.exe")
            QMessageBox.information(self, "完成", "资源管理器已重启")
        except Exception as e:
            QMessageBox.warning(self, "错误", str(e))
