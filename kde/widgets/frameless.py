"""
KDE Breeze 风格窗口装饰 - 无边框窗口 + 自绘标题栏。

特性：
    - FramelessHint 去掉 Windows 原生标题栏和边框
    - 自绘 Breeze 风格标题栏（图标、标题、最小化、最大化、关闭）
    - 窗口拖拽移动
    - 双击标题栏最大化/还原
    - Windows 原生 Aero Snap（拖到屏幕边缘自动半屏）
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ..theme import TITLEBAR_QSS


class BreezeTitleBar(QWidget):
    """Breeze 风格标题栏"""

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setStyleSheet(TITLEBAR_QSS)

        self._window = parent
        self._drag_pos = None
        self._is_maximized = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 窗口图标
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("padding-left: 6px; padding-right: 2px;")
        layout.addWidget(self.icon_label)

        # 标题
        self.title_label = QLabel(self)
        self.title_label.setObjectName("TitleLabel")
        layout.addWidget(self.title_label)

        layout.addStretch()

        # 最小化按钮
        self.btn_minimize = QPushButton("─", self)
        self.btn_minimize.setFixedSize(40, 30)
        self.btn_minimize.clicked.connect(self._on_minimize)
        layout.addWidget(self.btn_minimize)

        # 最大化/还原按钮
        self.btn_maximize = QPushButton("□", self)
        self.btn_maximize.setFixedSize(40, 30)
        self.btn_maximize.clicked.connect(self._on_maximize)
        layout.addWidget(self.btn_maximize)

        # 关闭按钮
        self.btn_close = QPushButton("✕", self)
        self.btn_close.setFixedSize(40, 30)
        self.btn_close.clicked.connect(self._on_close)
        layout.addWidget(self.btn_close)

    def set_title(self, title: str):
        self.title_label.setText(title)
        if self._window:
            self._window.setWindowTitle(title)

    def set_icon(self, icon: QIcon):
        if icon and not icon.isNull():
            pixmap = icon.pixmap(16, 16)
            self.icon_label.setPixmap(pixmap)

    def _on_minimize(self):
        if self._window:
            self._window.showMinimized()

    def _on_maximize(self):
        if self._window:
            if self._is_maximized:
                self._window.showNormal()
            else:
                self._window.showMaximized()

    def _on_close(self):
        if self._window:
            self._window.close()

    def set_maximized(self, maximized: bool):
        self._is_maximized = maximized
        self.btn_maximize.setText("❐" if maximized else "□")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.MouseButton.LeftButton:
            if self._window:
                if self._is_maximized:
                    self._window.showNormal()
                    new_x = event.globalPosition().toPoint().x() - self._window.width() // 2
                    self._window.move(new_x, 0)
                    self._drag_pos = event.globalPosition().toPoint()
                else:
                    delta = event.globalPosition().toPoint() - self._drag_pos
                    self._window.move(self._window.pos() + delta)
                    self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    def mouseDoubleClickEvent(self, event):
        self._on_maximize()
        event.accept()


class FramelessWindow(QWidget):
    """
    带 KDE Breeze 风格标题栏的无边框窗口。

    子类只需在 __init__ 里调用 self._setup_titlebar() 并添加内容到 self.content_layout。
    """

    def __init__(self, title: str = "KDEify", width: int = 800, height: int = 600):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        self._title_text = title

        # 根布局：垂直方向（标题栏在上，内容在下）
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # 标题栏
        self.titlebar = BreezeTitleBar(self)
        self.titlebar.set_title(title)
        self.root_layout.addWidget(self.titlebar)

        # 内容容器
        self.content_widget = QWidget(self)
        self.content_widget.setObjectName("ContentWidget")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.addWidget(self.content_widget)

        # 调整窗口大小
        self.resize(width, height)

        # 监听窗口状态
        self._was_maximized = False

    def set_content(self, widget: QWidget):
        """将内容控件放入内容区"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        self.content_layout.addWidget(widget)

    def set_window_icon(self, icon: QIcon):
        super().setWindowIcon(icon)
        self.titlebar.set_icon(icon)

    def set_window_title(self, title: str):
        super().setWindowTitle(title)
        self.titlebar.set_title(title)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        is_max = self.isMaximized()
        if is_max != self._was_maximized:
            self._was_maximized = is_max
            self.titlebar.set_maximized(is_max)

    def showMaximized(self):
        super().showMaximized()
        self.titlebar.set_maximized(True)

    def showNormal(self):
        super().showNormal()
        self.titlebar.set_maximized(False)
