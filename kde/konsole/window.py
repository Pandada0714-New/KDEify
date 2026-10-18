"""
Konsole 风格终端窗口 - 多标签页终端。
"""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QComboBox, QLineEdit,
    QFileDialog, QMessageBox, QToolBar,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction, QStyle

from ..widgets.frameless import FramelessWindow
from .terminal import TerminalWidget


class KonsoleWindow(FramelessWindow):
    """Konsole 风格终端"""

    def __init__(self):
        super().__init__("Konsole — KDEify", 760, 480)
        self._setup_titlebar()
        self._setup_ui()

    def _setup_titlebar(self):
        self.set_window_icon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

    def _setup_ui(self):
        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 工具栏
        toolbar = QToolBar(self)
        toolbar.setMovable(False)

        # Shell 选择
        toolbar.addWidget(QLabel("Shell: "))
        self.shell_combo = QComboBox(self)
        self.shell_combo.addItems(["cmd.exe", "powershell.exe", "wsl.exe"])
        self.shell_combo.currentTextChanged.connect(self._on_shell_changed)
        toolbar.addWidget(self.shell_combo)

        toolbar.addSeparator()

        # 新建标签页
        btn_new_tab = QPushButton("＋ 新标签页", self)
        btn_new_tab.clicked.connect(self._new_tab)
        toolbar.addWidget(btn_new_tab)

        # 关闭标签页
        btn_close_tab = QPushButton("✕ 关闭标签页", self)
        btn_close_tab.clicked.connect(self._close_current_tab)
        toolbar.addWidget(btn_close_tab)

        toolbar.addSeparator()

        # 字体大小
        toolbar.addWidget(QLabel("字号: "))
        self.font_combo = QComboBox(self)
        self.font_combo.addItems(["8", "9", "10", "11", "12", "14", "16"])
        self.font_combo.setCurrentText("10")
        self.font_combo.currentTextChanged.connect(self._on_font_changed)
        toolbar.addWidget(self.font_combo)

        layout.addWidget(toolbar)

        # 标签页控件
        self.tabs = QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self._on_tab_close_requested)
        layout.addWidget(self.tabs)

        # 初始标签页
        self._new_tab()

        self.set_content(central)

    def _new_tab(self):
        term = TerminalWidget(self)
        index = self.tabs.addTab(term, f"Shell {self.tabs.count() + 1}")
        self.tabs.setCurrentIndex(index)
        return term

    def _close_current_tab(self):
        if self.tabs.count() > 1:
            index = self.tabs.currentIndex()
            self.tabs.removeTab(index)
        else:
            self.close()

    def _on_tab_close_requested(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def _on_shell_changed(self, shell: str):
        """切换 shell：关闭当前标签页并新建"""
        current = self.tabs.currentWidget()
        if current:
            current.close()
            self.tabs.removeTab(self.tabs.currentIndex())
        term = TerminalWidget(self)
        term._shell = shell
        self.tabs.addTab(term, shell)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def _on_font_changed(self, size: str):
        current = self.tabs.currentWidget()
        if current:
            font = current.font()
            font.setPointSize(int(size))
            current.setFont(font)
